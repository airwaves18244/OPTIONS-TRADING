"""Option pricing models: Black-Scholes-Merton, CRR binomial, implied volatility.

All functions accept ``kind`` as ``"call"`` or ``"put"`` (lowercase; raise ``ValueError``
otherwise), time ``t`` in years, and annualized decimal ``vol``, ``rate``, ``div_yield``.
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

Kind = Literal["call", "put"]


def _check_kind(kind: str) -> None:
    if kind not in ("call", "put"):
        raise ValueError(f"kind must be 'call' or 'put', got {kind!r}")


def _intrinsic(kind: Kind, spot: float, strike: float) -> float:
    if kind == "call":
        return max(spot - strike, 0.0)
    return max(strike - spot, 0.0)


def bsm_price(
    kind: Kind,
    spot: float,
    strike: float,
    t: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> float:
    """European option price under Black-Scholes-Merton.

    Uses the standard BSM formulas with continuous dividend yield ``q``:

        d1 = (ln(S/K) + (r - q + vol^2/2) t) / (vol sqrt(t))
        d2 = d1 - vol sqrt(t)
        call = S e^{-q t} N(d1) - K e^{-r t} N(d2)
        put  = K e^{-r t} N(-d2) - S e^{-q t} N(-d1)

    Edge cases:
    - ``t <= 0`` or ``vol <= 0`` returns discounted intrinsic value
      ``max(S - K, 0)`` / ``max(K - S, 0)`` (no discounting when t <= 0).
    - ``spot <= 0`` or ``strike <= 0`` raises ``ValueError``.

    Returns the price per share (not per contract).
    """
    _check_kind(kind)
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")

    if t <= 0 or vol <= 0:
        # discounted intrinsic; no discounting when expired (t <= 0)
        if t <= 0:
            return _intrinsic(kind, spot, strike)
        # vol <= 0 but time remaining: value is discounted forward intrinsic
        fwd = spot * math.exp((rate - div_yield) * t)
        disc = math.exp(-rate * t)
        if kind == "call":
            return disc * max(fwd - strike, 0.0)
        return disc * max(strike - fwd, 0.0)

    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + (rate - div_yield + 0.5 * vol * vol) * t) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    disc_r = math.exp(-rate * t)
    disc_q = math.exp(-div_yield * t)
    if kind == "call":
        return spot * disc_q * norm.cdf(d1) - strike * disc_r * norm.cdf(d2)
    return strike * disc_r * norm.cdf(-d2) - spot * disc_q * norm.cdf(-d1)


def binomial_price(
    kind: Kind,
    spot: float,
    strike: float,
    t: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
    steps: int = 200,
    american: bool = True,
) -> float:
    """Cox-Ross-Rubinstein binomial tree price, American by default.

    With ``american=False`` converges to :func:`bsm_price` as ``steps`` grows
    (within ~1e-2 at 200 steps for typical inputs). With ``american=True`` the
    price is >= the European price (early-exercise premium, e.g. deep ITM puts).

    Same edge-case behavior as :func:`bsm_price` for ``t <= 0`` / ``vol <= 0``.
    ``steps < 1`` raises ``ValueError``. Returns price per share.
    """
    _check_kind(kind)
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if steps < 1:
        raise ValueError("steps must be >= 1")

    if t <= 0 or vol <= 0:
        return bsm_price(kind, spot, strike, t, vol, rate, div_yield)

    dt = t / steps
    u = math.exp(vol * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-rate * dt)
    p = (math.exp((rate - div_yield) * dt) - d) / (u - d)
    if p < 0 or p > 1:
        # numerically degenerate; fall back to BSM European value
        return bsm_price(kind, spot, strike, t, vol, rate, div_yield)

    j = np.arange(steps + 1)
    # terminal spot prices: S * u^j * d^(steps-j)
    prices = spot * u ** j * d ** (steps - j)
    if kind == "call":
        values = np.maximum(prices - strike, 0.0)
    else:
        values = np.maximum(strike - prices, 0.0)

    for i in range(steps, 0, -1):
        values = disc * (p * values[1:i + 1] + (1.0 - p) * values[0:i])
        if american:
            node_prices = spot * u ** np.arange(i) * d ** (i - 1 - np.arange(i))
            if kind == "call":
                exercise = np.maximum(node_prices - strike, 0.0)
            else:
                exercise = np.maximum(strike - node_prices, 0.0)
            values = np.maximum(values, exercise)

    return float(values[0])


def implied_vol(
    kind: Kind,
    price: float,
    spot: float,
    strike: float,
    t: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> float:
    """Implied volatility: the ``vol`` such that ``bsm_price(...) == price``.

    Solved with a bracketing root-finder (e.g. ``scipy.optimize.brentq``) on
    vol in roughly [1e-6, 10]. Raises ``ValueError`` when ``price`` is outside
    the no-arbitrage range (below discounted intrinsic or above the spot/strike
    bound) so no vol can reproduce it, or when ``t <= 0``.

    Round-trip property (tested): ``implied_vol(k, bsm_price(k, ..., vol=v), ...) ≈ v``.
    """
    _check_kind(kind)
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be positive")
    if t <= 0:
        raise ValueError("cannot imply vol at or past expiry (t <= 0)")

    disc_r = math.exp(-rate * t)
    disc_q = math.exp(-div_yield * t)
    # No-arbitrage bounds for European options.
    if kind == "call":
        lower = max(spot * disc_q - strike * disc_r, 0.0)
        upper = spot * disc_q
    else:
        lower = max(strike * disc_r - spot * disc_q, 0.0)
        upper = strike * disc_r

    tol = 1e-10
    if price < lower - 1e-9:
        raise ValueError("price below no-arbitrage lower bound; no vol reproduces it")
    if price > upper + 1e-9:
        raise ValueError("price above no-arbitrage upper bound; no vol reproduces it")
    if price <= lower + tol:
        # at intrinsic bound -> vol approaches 0
        raise ValueError("price at/below intrinsic bound; no positive vol reproduces it")

    def objective(vol: float) -> float:
        return bsm_price(kind, spot, strike, t, vol, rate, div_yield) - price

    lo, hi = 1e-6, 10.0
    if objective(lo) > 0:
        raise ValueError("price below achievable range for vol >= 1e-6")
    if objective(hi) < 0:
        # expand upper bracket
        hi = 50.0
        if objective(hi) < 0:
            raise ValueError("price above achievable range for vol <= 50")

    return float(brentq(objective, lo, hi, xtol=1e-12, rtol=1e-12, maxiter=200))
