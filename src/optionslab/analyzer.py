"""Strategy analytics: breakevens, max P/L, probability of profit, scenario grids.

Everything operates on a :class:`~optionslab.position.Position` and returns dollars
(P&L including entry premiums) unless stated otherwise.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

from optionslab.position import Position


def breakevens(pos: Position, spot_range: tuple[float, float] | None = None) -> list[float]:
    """Spot prices where expiry P&L crosses zero, ascending.

    Found numerically: sign changes of ``payoff.pnl_at_expiry`` on a dense grid
    (default grid from ``payoff.default_spot_grid``; ``spot_range=(lo, hi)``
    overrides), refined by bisection to ~1e-4. Tangent touches (P&L == 0 at an
    extremum without sign change) need not be reported. Empty list if the
    position never crosses zero in range.
    """
    raise NotImplementedError


def max_profit(pos: Position, spot_range: tuple[float, float] | None = None) -> float:
    """Maximum expiry P&L in dollars; ``math.inf`` when unbounded.

    Evaluated on a dense grid over ``spot_range`` (default: 0 to well beyond the
    highest strike). Unboundedness is detected from the P&L slope at the grid's
    upper boundary (positive slope => +inf; expiry P&L is piecewise linear beyond
    the last strike). The lower boundary is spot = 0, which the grid includes.
    """
    raise NotImplementedError


def max_loss(pos: Position, spot_range: tuple[float, float] | None = None) -> float:
    """Minimum expiry P&L in dollars (a loss is **negative**); ``-math.inf`` when
    unbounded (detected like :func:`max_profit`, negative slope at the upper edge)."""
    raise NotImplementedError


def expected_move(spot: float, vol: float, t: float) -> float:
    """1-sigma expected move in dollars: ``spot * vol * sqrt(t)``."""
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
