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

from dataclasses import dataclass

from optionslab.position import Position
from optionslab.pricing import Kind


@dataclass(frozen=True)
class Greeks:
    """Container for the five first-order greeks. Supports ``+`` and scalar ``*``."""

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

    def __add__(self, other: "Greeks") -> "Greeks":
        raise NotImplementedError

    def __mul__(self, scalar: float) -> "Greeks":
        raise NotImplementedError

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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
