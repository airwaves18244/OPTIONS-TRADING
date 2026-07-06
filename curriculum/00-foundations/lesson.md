# 00 — Foundations: Reading the Machine

You already know a call is the right to buy and a put is the right to sell. That is the
vocabulary. This module is the grammar: how the contract actually settles, why a premium is
the number it is, and how to read an option chain the way a mechanic reads an engine — knowing
which part does what before touching anything. When you finish, you will be able to take any
row in a chain and say, out loud and without code, *how much of this price is real value and
how much is hope, what happens to it as time passes, and what would have to be true for me to
be assigned early*. That fluency is the floor everything else in this curriculum stands on.

We anchor every example to the **DEMO** underlying: a stock trading at **$100** with implied
volatility around **25%**. Keep that picture in your head — a $100 stock — for the whole
module. Concrete beats abstract every time.

---

## 1. The contract, precisely

A US equity option is a standardized contract. One contract controls **100 shares** — the
**multiplier**. When a chain quotes a call at **3.91**, that is a price *per share*; the
contract costs **$391** (3.91 × 100) before commissions. This single fact is where most
beginners misjudge size: a "cheap" $1.19 option is $119 a contract, and ten of them is $1,190
of risk, not pocket change.

Every option has four defining attributes:

- **Kind** — call or put.
- **Strike** — the fixed price at which the contract can be exercised. DEMO lists strikes every
  $2.50: 90, 92.5, 95, 97.5, 100, 102.5, and so on.
- **Expiration** — the date the contract dies. We measure the runway to it as **DTE**
  (days-to-expiration). In this library, time is always expressed **in years**: 45 DTE is
  `45/365 ≈ 0.1233`. Burn that convention in now — every pricing call wants years, not days.
- **Style** — American (exercisable any time before expiration) or European (only at
  expiration). US equity options are **American**; most cash-settled index options (SPX, for
  example) are European. Style is not cosmetic; it is the entire reason early assignment exists.

### Notional vs. premium

The **notional** value an option controls is `strike × 100`. A 100-strike DEMO call controls
$10,000 of stock for a $391 premium. That leverage — roughly 25:1 of notional to premium here —
is the whole attraction and the whole danger of options. A 4% move in a $100 stock is $4; on
$10,000 notional that is $400, which can double or vaporize a $391 premium. Leverage does not
care which direction it works in.

---

## 2. Moneyness: where the strike sits relative to spot

**Moneyness** describes the strike's position against the current stock price (**spot**, $100
for DEMO).

- **In-the-money (ITM)** — the option has intrinsic value right now. A call is ITM when
  `spot > strike` (the 90 call, with spot at 100, is $10 ITM). A put is ITM when
  `spot < strike` (the 110 put is $10 ITM).
- **At-the-money (ATM)** — strike ≈ spot. The 100 strike is ATM.
- **Out-of-the-money (OTM)** — no intrinsic value. The 110 call and the 90 put are OTM at spot
  100.

Moneyness is not a label you memorize once; it *moves* as the stock moves. Today's OTM 105 call
becomes ATM if the stock rallies to 105 and ITM at 110. Everything about an option's behavior —
its greeks, its decay, its assignment risk — is a function of where spot sits relative to strike.

---

## 3. Intrinsic and extrinsic: the two halves of every premium

This is the single most important decomposition in the module. **Every option premium splits
into exactly two parts:**

```
premium = intrinsic value + extrinsic value
```

**Intrinsic value** is the exercise value locked in right now — what you would capture if the
option settled this instant:

- Call intrinsic = `max(spot − strike, 0)`
- Put intrinsic = `max(strike − spot, 0)`

It can never be negative. An OTM option has **zero** intrinsic value.

**Extrinsic value** (also called *time value*) is everything else — the premium above intrinsic.
It is the market's price for the *possibility* that the option finishes further in-the-money
before expiration. Extrinsic value is a function of three things: **time remaining**,
**implied volatility**, and how close the strike is to the money. It is the part that decays.
It is the part you *pay for* as a buyer and *collect* as a seller.

### Worked example (DEMO, 45 DTE)

Take three DEMO calls with spot at 100 and 45 days to run:

| Strike | Mid premium | Intrinsic | Extrinsic |
|-------:|------------:|----------:|----------:|
| 90 (ITM)  | 11.07 | 10.00 | 1.07 |
| 100 (ATM) | 3.91  | 0.00  | 3.91 |
| 110 (OTM) | 0.73  | 0.00  | 0.73 |

Read this table until it clicks. The deep-ITM 90 call is *mostly intrinsic* — it behaves almost
like owning stock, with a thin $1.07 of time value on top. The ATM 100 call is *pure extrinsic*:
every cent of its $3.91 is time value, which is why ATM options have the most to lose from the
passage of time. The OTM 110 call is *entirely extrinsic* too, but cheap, because the market
thinks a move above 110 in 45 days is a long shot. Notice the ATM option carries the **most
absolute extrinsic value** — the market charges the most for uncertainty exactly where the
outcome is most in doubt.

The same holds for puts. The 100 put at 45 DTE is 3.42, all extrinsic (near put-call parity
with the call, adjusted for carry). Do this decomposition reflexively for any option you look at.

---

## 4. Expiration, DTE, and the decay clock

Extrinsic value bleeds to zero at expiration — by definition, an expiring option is worth
exactly its intrinsic value. This bleed is **time decay** (theta, which module 01 treats in
full). Two things you must internalize now:

1. **Decay is not linear.** Extrinsic value erodes slowly when expiration is far off and
   *accelerates* as it approaches, roughly with the square root of time remaining. An ATM
   option loses time value fastest in its final week or two. The DEMO ATM call is worth 3.91 at
   45 DTE, ~2.66 at 21 DTE, ~1.52 at 7 DTE — the drop steepens as the clock runs out.
2. **Decay is the seller's income and the buyer's rent.** If you *own* an option, time is your
   enemy; nothing has to go wrong for you to lose money — the stock just has to sit still. If
   you *sold* it, time is your paycheck.

**Expiration cycles.** Liquid US names list weekly expirations (every Friday) plus standard
monthly expirations (the third Friday of each month) and sometimes quarterlies and LEAPS
(long-dated, up to ~2 years out). Monthlies are the most liquid; weeklies give precision around
events. DEMO's sample chain gives you 7, 21, 30, 45, 60, 90, and 180 DTE to work with.

---

## 5. Exercise, assignment, and settlement

**Exercise** is the holder invoking their right; **assignment** is what happens to a short on the
other side. When a call holder exercises, they buy 100 shares at the strike; a randomly assigned
short call *seller* must deliver 100 shares at the strike. Puts mirror this: the put holder sells
100 shares at the strike; the assigned short put seller must buy them.

**Settlement** in US equity options is **physical** — actual shares change hands. (Index options
like SPX are **cash-settled**: the difference is paid in cash, no shares, and they are European,
so no early assignment. Know which you are trading.)

**Automatic exercise.** At expiration, the Options Clearing Corporation auto-exercises any option
that is ITM by **$0.01 or more** (the "exercise-by-exception" rule) unless the holder instructs
otherwise. Practical consequence: if you are short an option that expires even a penny ITM, expect
to be assigned. If you are long, an ITM option you forgot about will turn into a 100-share stock
position (and the cash to pay for it) on Monday — a nasty surprise if you did not have the
capital. **Pin risk** is the special hazard of a stock closing *right at* your short strike:
you do not know until after the close whether you will be assigned, leaving you with an
unexpected, unhedged stock position over the weekend.

### Early assignment — the part everyone gets wrong

Because US equity options are American, a short option can be assigned **any day**, not just at
expiration. But in practice early assignment is **rare and predictable**, driven almost entirely
by one thing: **it only makes sense to exercise early when doing so captures more than the
extrinsic value you throw away.** Exercising kills the option's remaining time value, so a
rational holder does it only when something else pays them more.

The dominant case is **dividends and short calls.** A call holder who exercises the day before
the ex-dividend date converts to stock in time to collect the dividend. They will do this only
if the dividend they capture **exceeds the remaining extrinsic value** in the call — which
happens when the call is **deep ITM** (little time value left) and the dividend is meaningful.
So: if you are short a call on a dividend-paying stock, and the call is deep ITM as ex-dividend
approaches, and its remaining extrinsic value is *less than the dividend*, assume you will be
assigned the day before ex-date. Roll it or close it beforehand if you do not want the short
stock. This is the single most common early-assignment event retail sellers meet.

For **short puts**, early assignment is driven by interest/carry and by very deep-ITM puts whose
extrinsic value has collapsed — less common in low-rate environments but real. The general rule
holds: **check the option's remaining extrinsic value.** If a counterparty exercising early
would forfeit meaningful time value, they almost never do it. An option with $2 of extrinsic
left is not getting assigned early; a deep-ITM option with $0.03 of extrinsic and a dividend on
the horizon very well might.

DEMO pays no dividend in our examples, so we will flag dividend-driven assignment conceptually
and return to the mechanics in module 10.

---

## 6. Reading the chain

An **option chain** is the menu: every listed strike and expiration with its current quotes.
The `optionslab` sample chains carry these columns: `kind`, `strike`, `expiry_days`, `bid`,
`ask`, `mid`, `iv`, `volume`, `open_interest`, `spot`. Here is how to read each field like a
trader, not a spreadsheet.

- **bid / ask** — the best price someone will *pay* (bid) and the best price someone will *sell
  at* (ask). You buy at the ask, sell at the bid, in the absence of price improvement. The DEMO
  100 call shows 3.89 / 3.93.
- **mid** — the midpoint, `(bid + ask) / 2` = 3.91. This is the *fair* reference and roughly
  where a decent limit order fills on a liquid option. Never assume you transact at mid on an
  illiquid one.
- **bid-ask spread** — `ask − bid`. On the DEMO 100 call it is $0.04, tight and healthy. On the
  far OTM 130 call it is 0.00 / 0.02 — a spread as wide as the option is worth. The spread is a
  round-trip cost you pay twice (in and out); on wide markets it can dwarf your edge.
- **iv** — the implied volatility the market is pricing into *that specific strike*. Notice it is
  not constant across strikes (that is skew, module 02): the DEMO 65 put shows IV ~0.39 while the
  105 call shows ~0.256.
- **volume** — contracts traded *today*. A liquidity pulse.
- **open_interest** — contracts *currently outstanding* (opened but not yet closed). The deeper
  measure of liquidity. The DEMO 100 call shows OI over 8,000 — deep and tradeable.
- **spot** — the underlying price, repeated on every row (100 for DEMO).

### Liquidity: the filter you apply first

Before strategy, before greeks, ask: *can I get in and out at a fair price?* A beautiful setup on
an illiquid option is a trap — you will pay the spread coming and going and may not be able to
exit at all when it matters. Practical liquidity standards (revisited in module 10):

- **Tight spreads** — ideally the spread is a small fraction of the option's value (a few cents
  on a multi-dollar option). A market of 0.10 / 0.40 is unacceptable.
- **Real open interest** — hundreds to thousands of contracts, not single digits.
- **Volume** — some trades today, so a mid-price fill is realistic.

The DEMO chain is deliberately liquid near the money and thins out in the far wings — exactly like
a real name. Train yourself to *see* that thinning in the numbers.

---

## 7. Order types

You place option orders as **limit orders** almost without exception. A **market order** on an
option — especially anything but the most liquid strike — hands the market maker your wallet;
you fill at the ask (or worse) with no control. Use a **limit order** at or near mid and let it
work.

- **Limit order** — buy/sell at a specified price or better. Your default.
- **Market order** — execute immediately at prevailing prices. Avoid on options.
- **Stop / stop-limit** — triggers an order when the underlying (or option) hits a level. Useful
  for discipline, but option stops can trigger on a spread blip; use judiciously.
- **Multi-leg (combo) orders** — spreads are entered as *one* order with a single net
  debit/credit limit (e.g., "buy the 100/110 call spread for a net 1.20 debit"). This is
  essential: legging in one contract at a time exposes you to the market moving between fills.
  Every spread in modules 03–05 should be entered as a single combo order at a net price.

**Net debit vs. net credit.** When you build a multi-leg position, the premiums net out. If you
pay more than you collect, it is a **debit** (cash out of your account). If you collect more than
you pay, it is a **credit** (cash in). In this library, `Position.net_premium()` is **positive
for a debit and negative for a credit** — memorize that sign convention, because it flows through
every P&L number the analyzer reports.

---

## 8. What actually moves a premium

You can now name the inputs to an option's price. When a premium changes, exactly one (or more)
of these moved:

1. **Spot** — the stock moves. Directional. Measured by **delta** (and its speed, **gamma**).
   Up helps calls, hurts puts, and vice versa.
2. **Time passing** — always erodes extrinsic value. Measured by **theta**. Works against
   buyers, for sellers, every single day.
3. **Implied volatility** — the market's estimate of future movement. Rises inflate every
   option's extrinsic value; falls deflate it. Measured by **vega**. This is the input beginners
   ignore and professionals obsess over: you can be *right on direction and still lose* because
   IV collapsed (the "vol crush" after earnings, module 02).
4. **Interest rates** — a minor influence for most retail horizons. Measured by **rho**.
5. **Dividends** — lower call values and raise put values (and drive the early-assignment logic
   above).

Hold the mental model: an option's price is a small machine with these five dials. Turn spot,
turn time, turn vol — the premium responds in ways you can predict once you know the greeks.
**Module 01 is nothing but a careful tour of those dials.** The reason we decomposed premium into
intrinsic + extrinsic first is that the greeks all describe how the *extrinsic* part behaves —
intrinsic value just tracks the stock one-for-one.

---

## Key takeaways

- One equity option contract controls **100 shares**; a per-share premium of 3.91 is **$391** of
  cash. Always translate quotes into dollars and notional before sizing.
- **Every premium = intrinsic + extrinsic.** Intrinsic is locked-in exercise value
  (`max(S−K,0)` calls, `max(K−S,0)` puts); extrinsic is time/vol value that decays to zero at
  expiration. ATM options carry the most extrinsic value.
- **Time decay accelerates** into expiration and is the seller's income, the buyer's rent.
- US equity options are **American and physically settled**; the OCC auto-exercises anything ITM
  by ≥ $0.01. **Early assignment** is rare and rational — it happens mainly on **deep-ITM short
  calls before ex-dividend**, when the dividend captured exceeds the option's remaining extrinsic
  value.
- Read a chain by liquidity first: **tight bid-ask spreads, real open interest, some volume.**
  Trade at **mid via limit orders**; enter spreads as single **net-debit/credit combo orders**.
- `net_premium() > 0` is a **debit**, `< 0` a **credit** — the sign that drives every P&L number.
- A premium moves only when **spot, time, implied vol, rates, or dividends** move — the five
  dials the greeks measure.

## In the next module

We put numbers on the five dials: **the greeks** — delta, gamma, theta, vega, and rho — how each
one changes with moneyness, time, and volatility, and how they sum across the legs of a position.
