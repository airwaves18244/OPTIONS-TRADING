"""Strategy factories: named option structures as ready-made :class:`Position` objects.

Uniform conventions for every factory here:

- Each **option leg is a ``(strike, premium)`` tuple** (premium per share, >= 0).
  Parameter names say the role and direction, e.g. ``short_call=(110, 1.05)``.
- ``expiry`` is shared time-to-expiration in years; time-spread factories take
  per-leg expiries instead.
- ``quantity`` scales the whole structure (1 = one spread/condor/etc.); stock-based
  structures use ``100 * quantity`` shares per structure.
- Every factory validates strike ordering / strike equality where the structure
  requires it and raises ``ValueError`` on violation.
- Every factory sets a descriptive ``Position.label`` (e.g. ``"Iron Condor 85/90/110/115"``).

Legs given as long/short in the parameter name get the corresponding quantity sign.
"""

from __future__ import annotations

from optionslab.position import Position
from optionslab.pricing import Kind

LegSpec = tuple[float, float]
"""(strike, premium-per-share)"""


# --- single leg ------------------------------------------------------------


def long_call(call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Buy a call."""
    raise NotImplementedError


def long_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Buy a put."""
    raise NotImplementedError


def short_call(call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Sell a (naked) call."""
    raise NotImplementedError


def short_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Sell a (naked) put."""
    raise NotImplementedError


# --- stock combinations -----------------------------------------------------


def covered_call(
    stock_price: float, short_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Long ``100*quantity`` shares at ``stock_price`` + short calls against them."""
    raise NotImplementedError


def cash_secured_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short put (the 'cash-secured' part is account context, not a leg)."""
    raise NotImplementedError


def protective_put(
    stock_price: float, long_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Long stock + long put protection."""
    raise NotImplementedError


def collar(
    stock_price: float,
    long_put: LegSpec,
    short_call: LegSpec,
    *,
    expiry: float,
    quantity: int = 1,
) -> Position:
    """Long stock + protective put + covered call. Requires put strike < call strike."""
    raise NotImplementedError


# --- vertical spreads --------------------------------------------------------


def bull_call_spread(
    long_call: LegSpec, short_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Debit call vertical. Requires long strike < short strike."""
    raise NotImplementedError


def bear_put_spread(
    long_put: LegSpec, short_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Debit put vertical. Requires long strike > short strike."""
    raise NotImplementedError


def bull_put_spread(
    short_put: LegSpec, long_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Credit put vertical. Requires short strike > long strike."""
    raise NotImplementedError


def bear_call_spread(
    short_call: LegSpec, long_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Credit call vertical. Requires short strike < long strike."""
    raise NotImplementedError


# --- straddles / strangles ----------------------------------------------------


def long_straddle(call: LegSpec, put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Long call + long put, same strike (validated)."""
    raise NotImplementedError


def short_straddle(call: LegSpec, put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short call + short put, same strike (validated)."""
    raise NotImplementedError


def long_strangle(put: LegSpec, call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Long OTM put + long OTM call. Requires put strike < call strike."""
    raise NotImplementedError


def short_strangle(put: LegSpec, call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short put + short call. Requires put strike < call strike."""
    raise NotImplementedError


# --- wings ---------------------------------------------------------------------


def iron_condor(
    long_put: LegSpec,
    short_put: LegSpec,
    short_call: LegSpec,
    long_call: LegSpec,
    *,
    expiry: float,
    quantity: int = 1,
) -> Position:
    """Short put spread + short call spread. Strikes must be strictly ascending
    in the order long_put < short_put < short_call < long_call."""
    raise NotImplementedError


def iron_butterfly(
    long_put: LegSpec,
    short_put: LegSpec,
    short_call: LegSpec,
    long_call: LegSpec,
    *,
    expiry: float,
    quantity: int = 1,
) -> Position:
    """Iron condor whose short put and short call share one (body) strike (validated)."""
    raise NotImplementedError


def long_call_butterfly(
    low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """All-call fly: +1 low, -2 mid, +1 high. Strictly ascending strikes."""
    raise NotImplementedError


def long_put_butterfly(
    low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """All-put fly: +1 low, -2 mid, +1 high. Strictly ascending strikes."""
    raise NotImplementedError


def broken_wing_butterfly(
    kind: Kind, low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """+1/-2/+1 fly in calls or puts with (typically) unequal wings.
    Only ascending strikes are validated — wing symmetry is the trader's choice."""
    raise NotImplementedError


# --- time spreads -----------------------------------------------------------------


def calendar_spread(
    kind: Kind,
    strike: float,
    *,
    front_expiry: float,
    front_premium: float,
    back_expiry: float,
    back_premium: float,
    quantity: int = 1,
) -> Position:
    """Short front-month + long back-month, same strike and kind.
    Requires ``front_expiry < back_expiry``."""
    raise NotImplementedError


def diagonal_spread(
    kind: Kind,
    short: LegSpec,
    long: LegSpec,
    *,
    short_expiry: float,
    long_expiry: float,
    quantity: int = 1,
) -> Position:
    """Short nearer-dated at one strike + long longer-dated at another.
    Requires ``short_expiry < long_expiry`` and differing strikes."""
    raise NotImplementedError


def poor_mans_covered_call(
    long_call: LegSpec,
    short_call: LegSpec,
    *,
    long_expiry: float,
    short_expiry: float,
    quantity: int = 1,
) -> Position:
    """Deep-ITM long call (LEAPS stand-in for stock) + short nearer-dated OTM call.
    Requires ``short_expiry < long_expiry`` and long strike < short strike."""
    raise NotImplementedError


# --- ratio structures ----------------------------------------------------------------


def call_ratio_spread(
    long_call: LegSpec,
    short_call: LegSpec,
    *,
    expiry: float,
    ratio: tuple[int, int] = (1, 2),
    quantity: int = 1,
) -> Position:
    """Long ``ratio[0]`` lower-strike calls, short ``ratio[1]`` higher-strike calls
    (default 1x2). Requires long strike < short strike and ratio[1] > ratio[0] > 0."""
    raise NotImplementedError


def put_ratio_spread(
    long_put: LegSpec,
    short_put: LegSpec,
    *,
    expiry: float,
    ratio: tuple[int, int] = (1, 2),
    quantity: int = 1,
) -> Position:
    """Long higher-strike puts, short more lower-strike puts (default 1x2).
    Requires long strike > short strike."""
    raise NotImplementedError


def call_backspread(
    short_call: LegSpec,
    long_call: LegSpec,
    *,
    expiry: float,
    ratio: tuple[int, int] = (1, 2),
    quantity: int = 1,
) -> Position:
    """Short ``ratio[0]`` lower-strike calls, long ``ratio[1]`` higher-strike calls.
    Requires short strike < long strike."""
    raise NotImplementedError


def put_backspread(
    short_put: LegSpec,
    long_put: LegSpec,
    *,
    expiry: float,
    ratio: tuple[int, int] = (1, 2),
    quantity: int = 1,
) -> Position:
    """Short higher-strike puts, long more lower-strike puts.
    Requires short strike > long strike."""
    raise NotImplementedError


# --- exotic-ish combos ------------------------------------------------------------------


def jade_lizard(
    short_put: LegSpec,
    short_call: LegSpec,
    long_call: LegSpec,
    *,
    expiry: float,
    quantity: int = 1,
) -> Position:
    """Short put + short call spread. Requires put strike < short call strike < long call
    strike. (Classic construction wants total credit > call-spread width, killing upside
    risk — that's checked by the analyzer, not enforced here.)"""
    raise NotImplementedError


def custom(*legs, label: str = "Custom") -> Position:
    """Build a Position from raw :class:`OptionLeg` / :class:`StockLeg` objects."""
    raise NotImplementedError
