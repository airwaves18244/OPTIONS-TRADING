"""Strategy analytics: breakevens, max P/L, probability of profit, scenario grids.

Everything operates on a :class:`~optionslab.position.Position` and returns dollars
(P&L including entry premiums) unless stated otherwise.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
import pandas as pd

from optionslab.greeks import position_greeks
from optionslab.payoff import default_spot_grid, pnl_at, pnl_at_expiry
from optionslab.position import Position


def breakevens(pos: Position, spot_range: tuple[float, float] | None = None) -> list[float]:
    """Spot prices where expiry P&L crosses zero, ascending.

    Found numerically: sign changes of ``payoff.pnl_at_expiry`` on a dense grid
    (default grid from ``payoff.default_spot_grid``; ``spot_range=(lo, hi)``
    overrides), refined by bisection to ~1e-4. Tangent touches (P&L == 0 at an
    extremum without sign change) need not be reported. Empty list if the
    position never crosses zero in range.
    """
    if spot_range is not None:
        lo, hi = spot_range
        grid = np.linspace(lo, hi, 2001)
    else:
        grid = default_spot_grid(pos, points=2001)

    f = lambda s: pnl_at_expiry(pos, float(s))
    vals = np.array([f(s) for s in grid])

    roots: list[float] = []
    for i in range(len(grid) - 1):
        y0, y1 = vals[i], vals[i + 1]
        if y0 == 0.0:
            # exact zero at a node: report if it's a genuine crossing (neighbors differ in sign)
            prev = vals[i - 1] if i > 0 else 0.0
            if i > 0 and prev * y1 < 0:
                roots.append(float(grid[i]))
            continue
        if y0 * y1 < 0:
            a, b = float(grid[i]), float(grid[i + 1])
            fa, fb = y0, y1
            for _ in range(100):
                m = 0.5 * (a + b)
                fm = f(m)
                if abs(b - a) < 1e-5:
                    break
                if fa * fm <= 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            roots.append(0.5 * (a + b))

    roots.sort()
    # dedupe near-identical roots
    deduped: list[float] = []
    for r in roots:
        if not deduped or abs(r - deduped[-1]) > 1e-3:
            deduped.append(r)
    return deduped


def max_profit(pos: Position, spot_range: tuple[float, float] | None = None) -> float:
    """Maximum expiry P&L in dollars; ``math.inf`` when unbounded.

    Evaluated on a dense grid over ``spot_range`` (default: 0 to well beyond the
    highest strike). Unboundedness is detected from the P&L slope at the grid's
    upper boundary (positive slope => +inf; expiry P&L is piecewise linear beyond
    the last strike). The lower boundary is spot = 0, which the grid includes.
    """
    grid, vals = _expiry_grid(pos, spot_range)
    slope_hi = vals[-1] - vals[-2]
    if slope_hi > 1e-6:
        return math.inf
    return float(np.max(vals))


def max_loss(pos: Position, spot_range: tuple[float, float] | None = None) -> float:
    """Minimum expiry P&L in dollars (a loss is **negative**); ``-math.inf`` when
    unbounded (detected like :func:`max_profit`, negative slope at the upper edge)."""
    grid, vals = _expiry_grid(pos, spot_range)
    slope_hi = vals[-1] - vals[-2]
    if slope_hi < -1e-6:
        return -math.inf
    return float(np.min(vals))


def _reference_prices(pos: Position) -> list[float]:
    from optionslab.position import OptionLeg, StockLeg

    refs: list[float] = []
    for leg in pos.legs:
        if isinstance(leg, OptionLeg):
            refs.append(leg.strike)
        elif isinstance(leg, StockLeg):
            refs.append(leg.entry_price)
    return refs


def _expiry_grid(
    pos: Position, spot_range: tuple[float, float] | None
) -> tuple[np.ndarray, np.ndarray]:
    if spot_range is not None:
        lo, hi = spot_range
    else:
        refs = _reference_prices(pos)
        lo = 0.0
        hi = max(refs) * 3.0
    grid = np.linspace(lo, hi, 3001)
    vals = np.array([pnl_at_expiry(pos, float(s)) for s in grid])
    return grid, vals


def expected_move(spot: float, vol: float, t: float) -> float:
    """1-sigma expected move in dollars: ``spot * vol * sqrt(t)``."""
    return spot * vol * math.sqrt(t)


def probability_of_profit(
    pos: Position,
    spot: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> float:
    """P(expiry P&L > 0) under a lognormal terminal distribution, in [0, 1].

    Terminal spot at the position's **earliest option expiry** ``T`` is modeled as
    ``S_T = spot * exp((r - q - vol^2/2) T + vol sqrt(T) Z)``, Z ~ N(0,1).
    Computed by numeric integration of the profit indicator against the lognormal
    density on a wide grid (e.g. ±6 sigma in log space, >= 2000 points) — this
    handles arbitrary multi-breakeven payoffs. Expiry P&L uses
    ``payoff.pnl_at_expiry`` (same-expiry approximation for mixed expiries).
    """
    T = pos.earliest_expiry
    sigma = vol * math.sqrt(T)
    drift = (rate - div_yield - 0.5 * vol * vol) * T
    # log-space grid ±6 sigma around the median log-spot
    n = 4001
    z = np.linspace(-6.0, 6.0, n)
    log_s = math.log(spot) + drift + sigma * z
    s_grid = np.exp(log_s)
    # standard normal density of z; S_T = spot*exp(drift + sigma z)
    pdf = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    profit = np.array([1.0 if pnl_at_expiry(pos, float(s)) > 0 else 0.0 for s in s_grid])
    numerator = np.trapezoid(profit * pdf, z)
    denominator = np.trapezoid(pdf, z)
    return float(numerator / denominator)


def scenario_grid(
    pos: Position,
    spots: Sequence[float] | np.ndarray,
    days_forward: Sequence[int],
    vol: float,
    vol_shift: Sequence[float] | None = None,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> pd.DataFrame:
    """Mark-to-model P&L over a scenario grid — the adjustment-analysis engine.

    Tidy long-format DataFrame with columns ``spot``, ``days_forward``, ``vol``,
    ``pnl``: one row per (spot × day × vol) combination, where ``vol`` iterates
    over ``vol + shift for shift in vol_shift`` (default ``[0.0]``). P&L from
    ``payoff.pnl_at`` with ``t_elapsed = days/365``; days at/after an expiry
    value legs at intrinsic. ``days_forward`` entries must be >= 0.
    """
    if any(d < 0 for d in days_forward):
        raise ValueError("days_forward entries must be >= 0")
    shifts = list(vol_shift) if vol_shift is not None else [0.0]

    rows = []
    for s in np.asarray(spots, dtype=float):
        for d in days_forward:
            for shift in shifts:
                v = vol + shift
                pnl = pnl_at(pos, float(s), d / 365.0, v, rate, div_yield)
                rows.append(
                    {"spot": float(s), "days_forward": int(d), "vol": float(v), "pnl": pnl}
                )
    return pd.DataFrame(rows, columns=["spot", "days_forward", "vol", "pnl"])


def summarize(
    pos: Position,
    spot: float,
    vol: float,
    rate: float = 0.0,
    div_yield: float = 0.0,
) -> dict:
    """One-stop pre-trade summary dict with keys:

    ``label``, ``net_premium`` (dollars, +debit/-credit), ``breakevens`` (list),
    ``max_profit``, ``max_loss`` (dollars, ±inf where unbounded),
    ``probability_of_profit`` (0..1), ``expected_move`` (dollars, at earliest
    expiry), ``greeks`` (:class:`~optionslab.greeks.Greeks`, dollar-aggregated,
    at ``t_elapsed=0``), ``days_to_expiry`` (earliest expiry, in days).
    """
    T = pos.earliest_expiry
    return {
        "label": pos.label,
        "net_premium": pos.net_premium(),
        "breakevens": breakevens(pos),
        "max_profit": max_profit(pos),
        "max_loss": max_loss(pos),
        "probability_of_profit": probability_of_profit(pos, spot, vol, rate, div_yield),
        "expected_move": expected_move(spot, vol, T),
        "greeks": position_greeks(pos, spot, vol, rate, div_yield, t_elapsed=0.0),
        "days_to_expiry": T * 365.0,
    }
