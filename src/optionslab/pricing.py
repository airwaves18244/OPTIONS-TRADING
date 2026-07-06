"""Option pricing models: Black-Scholes-Merton, CRR binomial, implied volatility.

All functions accept ``kind`` as ``"call"`` or ``"put"`` (lowercase; raise ``ValueError``
otherwise), time ``t`` in years, and annualized decimal ``vol``, ``rate``, ``div_yield``.
"""

from __future__ import annotations

from typing import Literal

Kind = Literal["call", "put"]


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
