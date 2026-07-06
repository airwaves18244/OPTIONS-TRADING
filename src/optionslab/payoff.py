"""Position valuation: expiry payoff and mark-to-model P&L before expiry.

All results are **dollars for the whole position**. "P&L" always includes entry cash
flows (``Position.net_premium``); "payoff" is liquidation value only.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from optionslab.position import OptionLeg, Position, StockLeg
from optionslab.pricing import bsm_price


def payoff_at_expiry(pos: Position, spot: float) -> float:
    """Liquidation value in dollars if every leg were settled at ``spot``.

    Option legs at intrinsic value (× quantity × multiplier), stock legs at
    ``spot * quantity``. Entry premiums are **not** included.

    Caveat (documented for users): for mixed-expiry positions (calendars,
    diagonals) "all legs at intrinsic" is a simplification — use :func:`pnl_at`
    evaluated at the front leg's expiry instead.
    """
    total = 0.0
    for leg in pos.legs:
        if isinstance(leg, OptionLeg):
            total += leg.intrinsic(spot) * leg.quantity * leg.multiplier
        elif isinstance(leg, StockLeg):
            total += spot * leg.quantity
    return total


def pnl_at_expiry(pos: Position, spot: float) -> float:
    """Expiry P&L in dollars: ``payoff_at_expiry(pos, spot) - pos.net_premium()``."""
    return payoff_at_expiry(pos, spot) - pos.net_premium()


def pnl_at(
    pos: Position,
    spot: float,
    t_elapsed: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> float:
    """Mark-to-model P&L in dollars after ``t_elapsed`` years, at ``spot`` and flat ``vol``.

    Each option leg is revalued with ``pricing.bsm_price`` at remaining time
    ``max(leg.expiry - t_elapsed, 0)``; stock legs at ``spot``. Entry cash flows
    subtracted. ``pnl_at(pos, s, t_elapsed >= all expiries, ...)`` equals
    :func:`pnl_at_expiry` for same-expiry positions.
    """
    value = 0.0
    for leg in pos.legs:
        if isinstance(leg, OptionLeg):
            t_rem = max(leg.expiry - t_elapsed, 0.0)
            px = bsm_price(leg.kind, spot, leg.strike, t_rem, vol, rate, div_yield)
            value += px * leg.quantity * leg.multiplier
        elif isinstance(leg, StockLeg):
            value += spot * leg.quantity
    return value - pos.net_premium()


def pnl_curve(
    pos: Position,
    spots: Sequence[float] | np.ndarray,
    t_elapsed: float | None = None,
    vol: float | None = None,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> np.ndarray:
    """Vectorized P&L across ``spots``.

    With ``t_elapsed is None`` returns expiry P&L (:func:`pnl_at_expiry` per spot);
    otherwise mark-to-model (:func:`pnl_at`, which requires ``vol``; raises
    ``ValueError`` if ``vol`` is None). Returns ``np.ndarray`` shaped like ``spots``.
    """
    spots_arr = np.asarray(spots, dtype=float)
    if t_elapsed is None:
        result = np.array(
            [pnl_at_expiry(pos, float(s)) for s in spots_arr.ravel()], dtype=float
        )
    else:
        if vol is None:
            raise ValueError("vol is required for mark-to-model pnl_curve (t_elapsed given)")
        result = np.array(
            [pnl_at(pos, float(s), t_elapsed, vol, rate, div_yield) for s in spots_arr.ravel()],
            dtype=float,
        )
    return result.reshape(spots_arr.shape)


def default_spot_grid(pos: Position, points: int = 201) -> np.ndarray:
    """A sensible spot grid for plotting/analysis of ``pos``.

    Spans from 40% below the lowest reference price to 40% above the highest,
    where reference prices are option strikes and stock entry prices. Linear,
    ``points`` samples.
    """
    refs: list[float] = []
    for leg in pos.legs:
        if isinstance(leg, OptionLeg):
            refs.append(leg.strike)
        elif isinstance(leg, StockLeg):
            refs.append(leg.entry_price)
    lo = min(refs) * 0.6
    hi = max(refs) * 1.4
    return np.linspace(lo, hi, points)
