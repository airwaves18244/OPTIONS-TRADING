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

from optionslab.position import OptionLeg, Position, StockLeg
from optionslab.pricing import Kind

LegSpec = tuple[float, float]
"""(strike, premium-per-share)"""


def _opt(kind: Kind, spec: LegSpec, expiry: float, quantity: int) -> OptionLeg:
    strike, premium = spec
    return OptionLeg(kind, float(strike), expiry, quantity, float(premium))


def _fmt(x: float) -> str:
    return f"{x:g}"


# --- single leg ------------------------------------------------------------


def long_call(call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Buy a call."""
    leg = _opt("call", call, expiry, quantity)
    return Position(legs=(leg,), label=f"Long Call {_fmt(call[0])}")


def long_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Buy a put."""
    leg = _opt("put", put, expiry, quantity)
    return Position(legs=(leg,), label=f"Long Put {_fmt(put[0])}")


def short_call(call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Sell a (naked) call."""
    leg = _opt("call", call, expiry, -quantity)
    return Position(legs=(leg,), label=f"Short Call {_fmt(call[0])}")


def short_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Sell a (naked) put."""
    leg = _opt("put", put, expiry, -quantity)
    return Position(legs=(leg,), label=f"Short Put {_fmt(put[0])}")


# --- stock combinations -----------------------------------------------------


def covered_call(
    stock_price: float, short_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Long ``100*quantity`` shares at ``stock_price`` + short calls against them."""
    stock = StockLeg(100 * quantity, float(stock_price))
    leg = _opt("call", short_call, expiry, -quantity)
    return Position(legs=(stock, leg), label=f"Covered Call {_fmt(short_call[0])}")


def cash_secured_put(put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short put (the 'cash-secured' part is account context, not a leg)."""
    leg = _opt("put", put, expiry, -quantity)
    return Position(legs=(leg,), label=f"Cash-Secured Put {_fmt(put[0])}")


def protective_put(
    stock_price: float, long_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Long stock + long put protection."""
    stock = StockLeg(100 * quantity, float(stock_price))
    leg = _opt("put", long_put, expiry, quantity)
    return Position(legs=(stock, leg), label=f"Protective Put {_fmt(long_put[0])}")


def collar(
    stock_price: float,
    long_put: LegSpec,
    short_call: LegSpec,
    *,
    expiry: float,
    quantity: int = 1,
) -> Position:
    """Long stock + protective put + covered call. Requires put strike < call strike."""
    if not (long_put[0] < short_call[0]):
        raise ValueError("collar requires put strike < call strike")
    stock = StockLeg(100 * quantity, float(stock_price))
    put_leg = _opt("put", long_put, expiry, quantity)
    call_leg = _opt("call", short_call, expiry, -quantity)
    return Position(
        legs=(stock, put_leg, call_leg),
        label=f"Collar {_fmt(long_put[0])}/{_fmt(short_call[0])}",
    )


# --- vertical spreads --------------------------------------------------------


def bull_call_spread(
    long_call: LegSpec, short_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Debit call vertical. Requires long strike < short strike."""
    if not (long_call[0] < short_call[0]):
        raise ValueError("bull_call_spread requires long strike < short strike")
    legs = (_opt("call", long_call, expiry, quantity), _opt("call", short_call, expiry, -quantity))
    return Position(legs=legs, label=f"Bull Call Spread {_fmt(long_call[0])}/{_fmt(short_call[0])}")


def bear_put_spread(
    long_put: LegSpec, short_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Debit put vertical. Requires long strike > short strike."""
    if not (long_put[0] > short_put[0]):
        raise ValueError("bear_put_spread requires long strike > short strike")
    legs = (_opt("put", long_put, expiry, quantity), _opt("put", short_put, expiry, -quantity))
    return Position(legs=legs, label=f"Bear Put Spread {_fmt(long_put[0])}/{_fmt(short_put[0])}")


def bull_put_spread(
    short_put: LegSpec, long_put: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Credit put vertical. Requires short strike > long strike."""
    if not (short_put[0] > long_put[0]):
        raise ValueError("bull_put_spread requires short strike > long strike")
    legs = (_opt("put", short_put, expiry, -quantity), _opt("put", long_put, expiry, quantity))
    return Position(legs=legs, label=f"Bull Put Spread {_fmt(short_put[0])}/{_fmt(long_put[0])}")


def bear_call_spread(
    short_call: LegSpec, long_call: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """Credit call vertical. Requires short strike < long strike."""
    if not (short_call[0] < long_call[0]):
        raise ValueError("bear_call_spread requires short strike < long strike")
    legs = (_opt("call", short_call, expiry, -quantity), _opt("call", long_call, expiry, quantity))
    return Position(legs=legs, label=f"Bear Call Spread {_fmt(short_call[0])}/{_fmt(long_call[0])}")


# --- straddles / strangles ----------------------------------------------------


def long_straddle(call: LegSpec, put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Long call + long put, same strike (validated)."""
    if call[0] != put[0]:
        raise ValueError("long_straddle requires call and put at the same strike")
    legs = (_opt("call", call, expiry, quantity), _opt("put", put, expiry, quantity))
    return Position(legs=legs, label=f"Long Straddle {_fmt(call[0])}")


def short_straddle(call: LegSpec, put: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short call + short put, same strike (validated)."""
    if call[0] != put[0]:
        raise ValueError("short_straddle requires call and put at the same strike")
    legs = (_opt("call", call, expiry, -quantity), _opt("put", put, expiry, -quantity))
    return Position(legs=legs, label=f"Short Straddle {_fmt(call[0])}")


def long_strangle(put: LegSpec, call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Long OTM put + long OTM call. Requires put strike < call strike."""
    if not (put[0] < call[0]):
        raise ValueError("long_strangle requires put strike < call strike")
    legs = (_opt("put", put, expiry, quantity), _opt("call", call, expiry, quantity))
    return Position(legs=legs, label=f"Long Strangle {_fmt(put[0])}/{_fmt(call[0])}")


def short_strangle(put: LegSpec, call: LegSpec, *, expiry: float, quantity: int = 1) -> Position:
    """Short put + short call. Requires put strike < call strike."""
    if not (put[0] < call[0]):
        raise ValueError("short_strangle requires put strike < call strike")
    legs = (_opt("put", put, expiry, -quantity), _opt("call", call, expiry, -quantity))
    return Position(legs=legs, label=f"Short Strangle {_fmt(put[0])}/{_fmt(call[0])}")


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
    ks = (long_put[0], short_put[0], short_call[0], long_call[0])
    if not (ks[0] < ks[1] < ks[2] < ks[3]):
        raise ValueError("iron_condor requires strictly ascending strikes")
    legs = (
        _opt("put", long_put, expiry, quantity),
        _opt("put", short_put, expiry, -quantity),
        _opt("call", short_call, expiry, -quantity),
        _opt("call", long_call, expiry, quantity),
    )
    label = f"Iron Condor {_fmt(ks[0])}/{_fmt(ks[1])}/{_fmt(ks[2])}/{_fmt(ks[3])}"
    return Position(legs=legs, label=label)


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
    if short_put[0] != short_call[0]:
        raise ValueError("iron_butterfly requires short put and short call at the same strike")
    if not (long_put[0] < short_put[0] < long_call[0]):
        raise ValueError("iron_butterfly requires long_put < body < long_call")
    legs = (
        _opt("put", long_put, expiry, quantity),
        _opt("put", short_put, expiry, -quantity),
        _opt("call", short_call, expiry, -quantity),
        _opt("call", long_call, expiry, quantity),
    )
    label = f"Iron Butterfly {_fmt(long_put[0])}/{_fmt(short_put[0])}/{_fmt(long_call[0])}"
    return Position(legs=legs, label=label)


def long_call_butterfly(
    low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """All-call fly: +1 low, -2 mid, +1 high. Strictly ascending strikes."""
    if not (low[0] < mid[0] < high[0]):
        raise ValueError("long_call_butterfly requires strictly ascending strikes")
    legs = (
        _opt("call", low, expiry, quantity),
        _opt("call", mid, expiry, -2 * quantity),
        _opt("call", high, expiry, quantity),
    )
    label = f"Long Call Butterfly {_fmt(low[0])}/{_fmt(mid[0])}/{_fmt(high[0])}"
    return Position(legs=legs, label=label)


def long_put_butterfly(
    low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """All-put fly: +1 low, -2 mid, +1 high. Strictly ascending strikes."""
    if not (low[0] < mid[0] < high[0]):
        raise ValueError("long_put_butterfly requires strictly ascending strikes")
    legs = (
        _opt("put", low, expiry, quantity),
        _opt("put", mid, expiry, -2 * quantity),
        _opt("put", high, expiry, quantity),
    )
    label = f"Long Put Butterfly {_fmt(low[0])}/{_fmt(mid[0])}/{_fmt(high[0])}"
    return Position(legs=legs, label=label)


def broken_wing_butterfly(
    kind: Kind, low: LegSpec, mid: LegSpec, high: LegSpec, *, expiry: float, quantity: int = 1
) -> Position:
    """+1/-2/+1 fly in calls or puts with (typically) unequal wings.
    Only ascending strikes are validated — wing symmetry is the trader's choice."""
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    if not (low[0] < mid[0] < high[0]):
        raise ValueError("broken_wing_butterfly requires strictly ascending strikes")
    legs = (
        _opt(kind, low, expiry, quantity),
        _opt(kind, mid, expiry, -2 * quantity),
        _opt(kind, high, expiry, quantity),
    )
    label = f"Broken Wing {kind.title()} Butterfly {_fmt(low[0])}/{_fmt(mid[0])}/{_fmt(high[0])}"
    return Position(legs=legs, label=label)


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
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    if not (front_expiry < back_expiry):
        raise ValueError("calendar_spread requires front_expiry < back_expiry")
    legs = (
        OptionLeg(kind, float(strike), front_expiry, -quantity, float(front_premium)),
        OptionLeg(kind, float(strike), back_expiry, quantity, float(back_premium)),
    )
    return Position(legs=legs, label=f"Calendar Spread {kind.title()} {_fmt(strike)}")


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
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    if not (short_expiry < long_expiry):
        raise ValueError("diagonal_spread requires short_expiry < long_expiry")
    if short[0] == long[0]:
        raise ValueError("diagonal_spread requires differing strikes")
    legs = (
        OptionLeg(kind, float(short[0]), short_expiry, -quantity, float(short[1])),
        OptionLeg(kind, float(long[0]), long_expiry, quantity, float(long[1])),
    )
    label = f"Diagonal Spread {kind.title()} {_fmt(short[0])}/{_fmt(long[0])}"
    return Position(legs=legs, label=label)


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
    if not (short_expiry < long_expiry):
        raise ValueError("poor_mans_covered_call requires short_expiry < long_expiry")
    if not (long_call[0] < short_call[0]):
        raise ValueError("poor_mans_covered_call requires long strike < short strike")
    legs = (
        OptionLeg("call", float(long_call[0]), long_expiry, quantity, float(long_call[1])),
        OptionLeg("call", float(short_call[0]), short_expiry, -quantity, float(short_call[1])),
    )
    label = f"Poor Man's Covered Call {_fmt(long_call[0])}/{_fmt(short_call[0])}"
    return Position(legs=legs, label=label)


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
    n_long, n_short = ratio
    if not (n_short > n_long > 0):
        raise ValueError("call_ratio_spread requires ratio[1] > ratio[0] > 0 (short heavier)")
    if not (long_call[0] < short_call[0]):
        raise ValueError("call_ratio_spread requires long strike < short strike")
    legs = (
        _opt("call", long_call, expiry, n_long * quantity),
        _opt("call", short_call, expiry, -n_short * quantity),
    )
    label = f"Call Ratio Spread {n_long}x{n_short} {_fmt(long_call[0])}/{_fmt(short_call[0])}"
    return Position(legs=legs, label=label)


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
    n_long, n_short = ratio
    if not (n_short > n_long > 0):
        raise ValueError("put_ratio_spread requires ratio[1] > ratio[0] > 0 (short heavier)")
    if not (long_put[0] > short_put[0]):
        raise ValueError("put_ratio_spread requires long strike > short strike")
    legs = (
        _opt("put", long_put, expiry, n_long * quantity),
        _opt("put", short_put, expiry, -n_short * quantity),
    )
    label = f"Put Ratio Spread {n_long}x{n_short} {_fmt(long_put[0])}/{_fmt(short_put[0])}"
    return Position(legs=legs, label=label)


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
    n_short, n_long = ratio
    if not (n_long > n_short > 0):
        raise ValueError("call_backspread requires ratio[1] > ratio[0] > 0 (long heavier)")
    if not (short_call[0] < long_call[0]):
        raise ValueError("call_backspread requires short strike < long strike")
    legs = (
        _opt("call", short_call, expiry, -n_short * quantity),
        _opt("call", long_call, expiry, n_long * quantity),
    )
    label = f"Call Backspread {n_short}x{n_long} {_fmt(short_call[0])}/{_fmt(long_call[0])}"
    return Position(legs=legs, label=label)


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
    n_short, n_long = ratio
    if not (n_long > n_short > 0):
        raise ValueError("put_backspread requires ratio[1] > ratio[0] > 0 (long heavier)")
    if not (short_put[0] > long_put[0]):
        raise ValueError("put_backspread requires short strike > long strike")
    legs = (
        _opt("put", short_put, expiry, -n_short * quantity),
        _opt("put", long_put, expiry, n_long * quantity),
    )
    label = f"Put Backspread {n_short}x{n_long} {_fmt(short_put[0])}/{_fmt(long_put[0])}"
    return Position(legs=legs, label=label)


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
    if not (short_put[0] < short_call[0] < long_call[0]):
        raise ValueError(
            "jade_lizard requires put strike < short call strike < long call strike"
        )
    legs = (
        _opt("put", short_put, expiry, -quantity),
        _opt("call", short_call, expiry, -quantity),
        _opt("call", long_call, expiry, quantity),
    )
    label = (
        f"Jade Lizard {_fmt(short_put[0])}/{_fmt(short_call[0])}/{_fmt(long_call[0])}"
    )
    return Position(legs=legs, label=label)


def custom(*legs, label: str = "Custom") -> Position:
    """Build a Position from raw :class:`OptionLeg` / :class:`StockLeg` objects."""
    return Position(legs=tuple(legs), label=label)
