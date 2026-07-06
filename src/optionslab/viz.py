"""Matplotlib visualizations: payoff diagrams, greeks curves, scenario heatmaps.

All functions accept an optional ``ax`` (created via ``plt.subplots()`` when None)
and **return the Axes** so plots compose. No ``plt.show()`` inside library code.
Style: horizontal zero line, breakevens as dotted verticals, profit region shaded
lightly green / loss red where practical, title from ``Position.label``.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from optionslab.position import Position


def plot_payoff(
    pos: Position,
    spots: Sequence[float] | np.ndarray | None = None,
    *,
    spot: float | None = None,
    vol: float | None = None,
    t_elapsed: float = 0.0,
    rate: float = 0.0,
    div_yield: float = 0.0,
    ax: Axes | None = None,
) -> Axes:
    """Expiry P&L line (solid) with optional mark-to-model "now" curve.

    ``spots`` defaults to ``payoff.default_spot_grid(pos)``. If ``vol`` is given,
    also draws the T+``t_elapsed`` model curve (dashed) via ``payoff.pnl_curve``.
    If ``spot`` is given, marks it with a vertical line. Annotates breakevens.
    """
    raise NotImplementedError


def plot_greeks(
    pos: Position,
    spots: Sequence[float] | np.ndarray | None = None,
    *,
    vol: float,
    t_elapsed: float = 0.0,
    rate: float = 0.0,
    div_yield: float = 0.0,
    which: Sequence[str] = ("delta", "gamma", "theta", "vega"),
    ax: Axes | None = None,
) -> Axes:
    """Position greeks (dollar-aggregated) as curves vs spot, one line per greek
    in ``which`` (each normalized to its own scale is NOT required — plot raw
    values; users pick subsets when scales clash)."""
    raise NotImplementedError


def plot_pnl_heatmap(grid: pd.DataFrame, *, ax: Axes | None = None) -> Axes:
    """Heatmap of an ``analyzer.scenario_grid`` result: spot on x, days_forward on y,
    color = pnl (diverging colormap centered at 0). If the grid contains multiple
    vols, uses the base (first) vol and ignores the rest."""
    raise NotImplementedError


def plot_compare(
    positions: Sequence[Position],
    spots: Sequence[float] | np.ndarray | None = None,
    *,
    ax: Axes | None = None,
) -> Axes:
    """Overlay expiry P&L curves of several candidate structures, legend from labels.
    ``spots`` defaults to the union span of the positions' default grids."""
    raise NotImplementedError
