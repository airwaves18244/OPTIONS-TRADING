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
        if self.kind not in ("call", "put"):
            raise ValueError(f"kind must be 'call' or 'put', got {self.kind!r}")
        if self.strike <= 0:
            raise ValueError("strike must be > 0")
        if self.expiry <= 0:
            raise ValueError("expiry must be > 0 (years)")
        if self.quantity == 0:
            raise ValueError("quantity must be nonzero")
        if self.premium < 0:
            raise ValueError("premium must be >= 0")
        if self.multiplier <= 0:
            raise ValueError("multiplier must be > 0")

    @property
    def entry_cash_flow(self) -> float:
        """Dollars paid at entry for this leg (positive = debit, negative = credit).

        ``premium * quantity * multiplier``.
        """
        return self.premium * self.quantity * self.multiplier

    def intrinsic(self, spot: float) -> float:
        """Intrinsic value per share at ``spot``: max(S-K, 0) for calls, max(K-S, 0) for puts."""
        if self.kind == "call":
            return max(spot - self.strike, 0.0)
        return max(self.strike - spot, 0.0)


@dataclass(frozen=True)
class StockLeg:
    """A stock leg: ``quantity`` shares (signed), bought/shorted at ``entry_price`` (> 0)."""

    quantity: int
    entry_price: float

    def __post_init__(self) -> None:
        if self.quantity == 0:
            raise ValueError("quantity must be nonzero")
        if self.entry_price <= 0:
            raise ValueError("entry_price must be > 0")

    @property
    def entry_cash_flow(self) -> float:
        """Dollars paid at entry: ``entry_price * quantity``."""
        return self.entry_price * self.quantity


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
        legs = tuple(self.legs)
        if len(legs) == 0:
            raise ValueError("Position must have at least one leg")
        object.__setattr__(self, "legs", legs)

    def __iter__(self) -> Iterator[Leg]:
        return iter(self.legs)

    @property
    def option_legs(self) -> tuple[OptionLeg, ...]:
        """Only the option legs, in order."""
        return tuple(leg for leg in self.legs if isinstance(leg, OptionLeg))

    @property
    def stock_legs(self) -> tuple[StockLeg, ...]:
        """Only the stock legs, in order."""
        return tuple(leg for leg in self.legs if isinstance(leg, StockLeg))

    def net_premium(self) -> float:
        """Total entry cash flow in dollars: positive = net debit, negative = net credit."""
        return sum(leg.entry_cash_flow for leg in self.legs)

    @property
    def earliest_expiry(self) -> float:
        """Smallest ``expiry`` among option legs. Raises ``ValueError`` if no option legs."""
        opts = self.option_legs
        if not opts:
            raise ValueError("Position has no option legs")
        return min(leg.expiry for leg in opts)

    def describe(self) -> str:
        """Multi-line human-readable summary: label, each leg, net debit/credit."""
        lines: list[str] = []
        if self.label:
            lines.append(self.label)
        for leg in self.legs:
            if isinstance(leg, OptionLeg):
                side = "long" if leg.quantity > 0 else "short"
                lines.append(
                    f"  {side} {abs(leg.quantity)}x {leg.kind} "
                    f"{leg.strike:g} @ {leg.premium:g} "
                    f"({leg.expiry * 365:.0f} DTE)"
                )
            else:
                side = "long" if leg.quantity > 0 else "short"
                lines.append(
                    f"  {side} {abs(leg.quantity)} shares @ {leg.entry_price:g}"
                )
        net = self.net_premium()
        if net > 0:
            lines.append(f"  net debit ${net:.2f}")
        elif net < 0:
            lines.append(f"  net credit ${-net:.2f}")
        else:
            lines.append("  net $0.00")
        return "\n".join(lines)
