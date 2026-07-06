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
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import TwoSlopeNorm

from optionslab import analyzer
from optionslab.greeks import position_greeks
from optionslab.payoff import default_spot_grid, pnl_curve
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
    if ax is None:
        _, ax = plt.subplots()
    if spots is None:
        spots = default_spot_grid(pos)
    spots = np.asarray(spots, dtype=float)

    expiry_pnl = pnl_curve(pos, spots)
    ax.plot(spots, expiry_pnl, color="C0", lw=2, label="Expiry P&L")
    ax.fill_between(spots, expiry_pnl, 0, where=expiry_pnl >= 0, color="green", alpha=0.12)
    ax.fill_between(spots, expiry_pnl, 0, where=expiry_pnl < 0, color="red", alpha=0.12)

    if vol is not None:
        mtm = pnl_curve(pos, spots, t_elapsed=t_elapsed, vol=vol, rate=rate, div_yield=div_yield)
        ax.plot(spots, mtm, color="C1", lw=1.5, ls="--", label="Now (mark-to-model)")

    ax.axhline(0, color="black", lw=0.8)

    for be in analyzer.breakevens(pos, spot_range=(float(spots.min()), float(spots.max()))):
        ax.axvline(be, color="grey", ls=":", lw=1)

    if spot is not None:
        ax.axvline(spot, color="black", ls="-.", lw=1, label="Spot")

    ax.set_xlabel("Spot price")
    ax.set_ylabel("P&L ($)")
    ax.set_title(pos.label or "Payoff")
    ax.legend()
    return ax


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
    if ax is None:
        _, ax = plt.subplots()
    if spots is None:
        spots = default_spot_grid(pos)
    spots = np.asarray(spots, dtype=float)

    for name in which:
        ys = np.array(
            [
                getattr(
                    position_greeks(pos, float(s), vol, rate, div_yield, t_elapsed),
                    name,
                )
                for s in spots
            ]
        )
        ax.plot(spots, ys, label=name)

    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("Spot price")
    ax.set_ylabel("Greek (dollar-aggregated)")
    ax.set_title(f"Greeks: {pos.label}" if pos.label else "Greeks")
    ax.legend()
    return ax


def plot_pnl_heatmap(grid: pd.DataFrame, *, ax: Axes | None = None) -> Axes:
    """Heatmap of an ``analyzer.scenario_grid`` result: spot on x, days_forward on y,
    color = pnl (diverging colormap centered at 0). If the grid contains multiple
    vols, uses the base (first) vol and ignores the rest."""
    if ax is None:
        _, ax = plt.subplots()

    base_vol = grid["vol"].iloc[0]
    sub = grid[np.isclose(grid["vol"], base_vol)]

    pivot = sub.pivot_table(index="days_forward", columns="spot", values="pnl")
    spots = pivot.columns.to_numpy()
    days = pivot.index.to_numpy()
    z = pivot.to_numpy()

    vmax = np.nanmax(np.abs(z))
    if vmax == 0 or not np.isfinite(vmax):
        vmax = 1.0
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)

    mesh = ax.pcolormesh(spots, days, z, cmap="RdYlGn", norm=norm, shading="auto")
    ax.figure.colorbar(mesh, ax=ax, label="P&L ($)")
    ax.set_xlabel("Spot price")
    ax.set_ylabel("Days forward")
    ax.set_title("Scenario P&L")
    return ax


def plot_compare(
    positions: Sequence[Position],
    spots: Sequence[float] | np.ndarray | None = None,
    *,
    ax: Axes | None = None,
) -> Axes:
    """Overlay expiry P&L curves of several candidate structures, legend from labels.
    ``spots`` defaults to the union span of the positions' default grids."""
    if ax is None:
        _, ax = plt.subplots()

    if spots is None:
        lo = min(float(default_spot_grid(p).min()) for p in positions)
        hi = max(float(default_spot_grid(p).max()) for p in positions)
        spots = np.linspace(lo, hi, 201)
    spots = np.asarray(spots, dtype=float)

    for i, pos in enumerate(positions):
        ys = pnl_curve(pos, spots)
        ax.plot(spots, ys, label=pos.label or f"Structure {i + 1}")

    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("Spot price")
    ax.set_ylabel("Expiry P&L ($)")
    ax.set_title("Structure comparison")
    ax.legend()
    return ax
