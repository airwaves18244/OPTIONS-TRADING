"""Position building blocks: option legs, stock legs, and multi-leg positions.

A ``Position`` is just an immutable bag of legs. Direction lives in each leg's
``quantity`` sign (positive = long, negative = short). All dollar aggregation
(premium, P&L, greeks) happens in ``payoff``/``analyzer``/``greeks`` using
``quantity * multiplier`` for options and ``quantity`` (shares) for stock.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Literal, Union


@dataclass(frozen=True)
class OptionLeg:
    """One option leg.

    Attributes:
        kind: ``"call"`` or ``"put"``.
        strike: strike price, > 0.
        expiry: time to expiration **in years at position entry** (45 DTE == 45/365), > 0.
        quantity: contracts; positive = long, negative = short; nonzero.
        premium: entry price **per share**, >= 0 (direction comes from ``quantity``).
        multiplier: shares per contract, default 100.

    ``__post_init__`` validates all of the above and raises ``ValueError`` on violation.
    """

    kind: Literal["call", "put"]
    strike: float
    expiry: float
    quantity: int
    premium: float
    multiplier: int = 100

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def entry_cash_flow(self) -> float:
        """Dollars paid at entry for this leg (positive = debit, negative = credit).

        ``premium * quantity * multiplier``.
        """
        raise NotImplementedError

    def intrinsic(self, spot: float) -> float:
        """Intrinsic value per share at ``spot``: max(S-K, 0) for calls, max(K-S, 0) for puts."""
        raise NotImplementedError


@dataclass(frozen=True)
class StockLeg:
    """A stock leg: ``quantity`` shares (signed), bought/shorted at ``entry_price`` (> 0)."""

    quantity: int
    entry_price: float

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def entry_cash_flow(self) -> float:
        """Dollars paid at entry: ``entry_price * quantity``."""
        raise NotImplementedError


Leg = Union[OptionLeg, StockLeg]


@dataclass(frozen=True)
class Position:
    """An immutable multi-leg position.

    Attributes:
        legs: tuple of :class:`OptionLeg` / :class:`StockLeg` (any iterable accepted
            at construction and normalized to a tuple; must be non-empty).
        label: human-friendly name (factories in ``strategies`` set this).
    """

    legs: tuple[Leg, ...]
    label: str = ""

    def __post_init__(self) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Leg]:
        raise NotImplementedError

    @property
    def option_legs(self) -> tuple[OptionLeg, ...]:
        """Only the option legs, in order."""
        raise NotImplementedError

    @property
    def stock_legs(self) -> tuple[StockLeg, ...]:
        """Only the stock legs, in order."""
        raise NotImplementedError

    def net_premium(self) -> float:
        """Total entry cash flow in dollars: positive = net debit, negative = net credit."""
        raise NotImplementedError

    @property
    def earliest_expiry(self) -> float:
        """Smallest ``expiry`` among option legs. Raises ``ValueError`` if no option legs."""
        raise NotImplementedError

    def describe(self) -> str:
        """Multi-line human-readable summary: label, each leg, net debit/credit."""
        raise NotImplementedError
