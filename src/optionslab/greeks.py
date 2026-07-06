"""Greeks: analytic BSM greeks, numeric fallback, and position-level aggregation.

Conventions (binding):
- ``delta``: per $1 spot move, per share.
- ``gamma``: change of delta per $1 spot move.
- ``theta``: price change per **calendar day** (annual theta / 365) — typically negative
  for long options.
- ``vega``: price change per **1 vol point** (IV +0.01).
- ``rho``: price change per **+1%** (0.01) rate move.

Per-share for single options; **dollar-aggregated** (× quantity × multiplier) for positions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.stats import norm

from optionslab.position import OptionLeg, Position, StockLeg
from optionslab.pricing import Kind, bsm_price


@dataclass(frozen=True)
class Greeks:
    """Container for the five first-order greeks. Supports ``+`` and scalar ``*``."""

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

    def __add__(self, other: "Greeks") -> "Greeks":
        return Greeks(
            self.delta + other.delta,
            self.gamma + other.gamma,
            self.theta + other.theta,
            self.vega + other.vega,
            self.rho + other.rho,
        )

    def __mul__(self, scalar: float) -> "Greeks":
        return Greeks(
            self.delta * scalar,
            self.gamma * scalar,
            self.theta * scalar,
            self.vega * scalar,
            self.rho * scalar,
        )

    __rmul__ = __mul__


def bsm_greeks(
    kind: Kind,
    spot: float,
    strike: float,
    t: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> Greeks:
    """Analytic BSM greeks per share, in the conventions above.

    For ``t <= 0`` or ``vol <= 0`` returns intrinsic-limit greeks: delta is 0 / ±1
    depending on moneyness (0.5 sign-adjusted exactly ATM), all others 0.
    """
    if kind not in ("call", "put"):
        raise ValueError(f"kind must be 'call' or 'put', got {kind!r}")
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")

    if t <= 0 or vol <= 0:
        if spot > strike:
            delta = 1.0 if kind == "call" else 0.0
        elif spot < strike:
            delta = 0.0 if kind == "call" else -1.0
        else:
            delta = 0.5 if kind == "call" else -0.5
        return Greeks(delta, 0.0, 0.0, 0.0, 0.0)

    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + (rate - div_yield + 0.5 * vol * vol) * t) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    disc_q = math.exp(-div_yield * t)
    disc_r = math.exp(-rate * t)
    pdf_d1 = norm.pdf(d1)

    gamma = disc_q * pdf_d1 / (spot * vol * sqrt_t)
    vega_annual = spot * disc_q * pdf_d1 * sqrt_t  # per 1.0 vol
    vega = vega_annual * 0.01  # per 1 vol point (0.01)

    if kind == "call":
        delta = disc_q * norm.cdf(d1)
        theta_annual = (
            -spot * disc_q * pdf_d1 * vol / (2 * sqrt_t)
            - rate * strike * disc_r * norm.cdf(d2)
            + div_yield * spot * disc_q * norm.cdf(d1)
        )
        rho_annual = strike * t * disc_r * norm.cdf(d2)
    else:
        delta = -disc_q * norm.cdf(-d1)
        theta_annual = (
            -spot * disc_q * pdf_d1 * vol / (2 * sqrt_t)
            + rate * strike * disc_r * norm.cdf(-d2)
            - div_yield * spot * disc_q * norm.cdf(-d1)
        )
        rho_annual = -strike * t * disc_r * norm.cdf(-d2)

    theta = theta_annual / 365.0  # per calendar day
    rho = rho_annual * 0.01  # per 1% rate move
    return Greeks(delta, gamma, theta, vega, rho)


def numeric_greeks(
    kind: Kind,
    spot: float,
    strike: float,
    t: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
    pricer=None,
) -> Greeks:
    """Finite-difference greeks using ``pricer`` (defaults to ``pricing.bsm_price``).

    Central differences for delta/gamma/vega/rho, one-day forward step for theta.
    Agrees with :func:`bsm_greeks` to ~1e-3 when using the BSM pricer (tested).
    Useful for American/binomial pricing where no analytic greeks exist.
    """
    if kind not in ("call", "put"):
        raise ValueError(f"kind must be 'call' or 'put', got {kind!r}")
    if pricer is None:
        pricer = bsm_price

    def price(s: float, k: float, tt: float, v: float, r: float, q: float) -> float:
        return pricer(kind, s, k, tt, v, r, q)

    ds = spot * 1e-4
    dv = 1e-4
    dr = 1e-4

    base = price(spot, strike, t, vol, rate, div_yield)

    up = price(spot + ds, strike, t, vol, rate, div_yield)
    dn = price(spot - ds, strike, t, vol, rate, div_yield)
    delta = (up - dn) / (2 * ds)
    gamma = (up - 2 * base + dn) / (ds * ds)

    v_up = price(spot, strike, t, vol + dv, rate, div_yield)
    v_dn = price(spot, strike, t, vol - dv, rate, div_yield)
    vega_per_vol = (v_up - v_dn) / (2 * dv)
    vega = vega_per_vol * 0.01  # per 1 vol point

    r_up = price(spot, strike, t, vol, rate + dr, div_yield)
    r_dn = price(spot, strike, t, vol, rate - dr, div_yield)
    rho_per_rate = (r_up - r_dn) / (2 * dr)
    rho = rho_per_rate * 0.01  # per 1% rate move

    # theta: one calendar day forward step
    dt = 1.0 / 365.0
    t_fwd = max(t - dt, 0.0)
    theta = price(spot, strike, t_fwd, vol, rate, div_yield) - base

    return Greeks(delta, gamma, theta, vega, rho)


def position_greeks(
    pos: Position,
    spot: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
    t_elapsed: float = 0.0,
) -> Greeks:
    """Aggregate dollar greeks of a position.

    Each option leg contributes ``bsm_greeks(...) * quantity * multiplier`` evaluated at
    remaining time ``max(leg.expiry - t_elapsed, 0)`` with the shared flat ``vol``.
    Stock legs contribute ``delta = quantity`` (shares), other greeks 0.
    """
    total = Greeks(0.0, 0.0, 0.0, 0.0, 0.0)
    for leg in pos.legs:
        if isinstance(leg, OptionLeg):
            t_rem = max(leg.expiry - t_elapsed, 0.0)
            g = bsm_greeks(leg.kind, spot, leg.strike, t_rem, vol, rate, div_yield)
            total = total + g * (leg.quantity * leg.multiplier)
        elif isinstance(leg, StockLeg):
            total = total + Greeks(float(leg.quantity), 0.0, 0.0, 0.0, 0.0)
    return total
