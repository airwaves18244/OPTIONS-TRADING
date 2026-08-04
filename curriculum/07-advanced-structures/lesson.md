# 07 — Advanced Structures: Shaping Risk Asymmetrically

Verticals and condors are *symmetric* in spirit: defined risk, defined reward, a clean box. The
structures in this module deliberately break the symmetry. A ratio spread finances extra short
options with a long one, buying you a fat profit zone at the cost of an open tail. A backspread does
the reverse — it pays a little to own *net long* options for a violent move. A broken-wing butterfly
slides one wing out to erase risk on one side entirely, sometimes for a net credit. A jade lizard
staples a short put to a short call spread so that, done right, there is **no risk to the upside at
all**. Each is an exercise in the same question: *you can reshape a payoff any way you like — but you
always pay for the good part somewhere. Where did the risk go, and can you live with it there?*
After this module you can build all six, read where their risk is buried, and judge when the extra
complexity is actually worth it.

---

## Concepts / Mechanics

### Ratios and the naked tail

A **ratio spread** is unbalanced: you are long some options and short *more* of them at a different
strike. The classic **1×2 call ratio** is long one lower-strike call and short two higher-strike
calls (`call_ratio_spread(long_call, short_call, ratio=(1, 2))`). The single long call and one of the
shorts form a normal bull call spread; the *extra* short call is **naked**. That naked call is the
whole story: above the short strike your losses grow without bound (or, for a put ratio, all the way
to zero). In exchange, the premium from two shorts can fully finance the long — many ratio spreads
go on for **even money or a credit**, giving you a wide zone where you make money and *no loss at all*
if the stock simply drifts to the short strike.

Sign convention reminder: `quantity` carries direction. A 1×2 call ratio has `+1` at the long strike
and `-2` at the short strike; net the structure is **short one call's worth of tail risk**.

### Backspreads: paying for convexity

A **backspread** flips the ratio: short the *nearer* strike, long *more* of the farther strike
(`call_backspread(short_call, long_call, ratio=(1, 2))` → short one lower call, long two higher
calls). Now you are **net long** options and **long gamma**: a big move in your direction pays off
convexly, and the single short leg helps fund the two longs so the trade can be cheap or free. The
price you pay is a **valley** — a zone of moderate adverse movement where both the short is ITM and
your longs have not yet caught up, which is where the backspread takes its (defined) maximum loss.
Backspreads are **long-vega, long-tail** trades: they want a *cheap* entry (low IV) and a big
directional break, and they bleed if the stock sits still.

### The broken wing: moving risk off one side

A standard butterfly (+1 / −2 / +1, equal wing widths) is symmetric and pays a small debit for a peak
at the body. A **broken-wing butterfly (BWB)** keeps the +1 / −2 / +1 skeleton but makes the wings
**unequal** — you push one long strike farther out
(`broken_wing_butterfly(kind, low, mid, high, ...)`, ascending strikes, widths your choice). Widening
the *far* wing reduces the cost of that wing, which can turn the whole fly into a **credit** and
**eliminate risk on the near side** entirely: if the stock goes the "safe" way, the worst case is you
keep the credit. The catch: the side with the *wider* wing now carries the risk — the gap between the
body and the distant long strike is unhedged over that span, so a move that direction hits your
defined max loss. A BWB is how you say "I'm neutral-to-slightly-directional, and I want to be paid to
be wrong in one specific direction."

### The jade lizard: erasing upside risk

A **jade lizard** is a short put plus a short call spread
(`jade_lizard(short_put, short_call, long_call)`): you sell a put below the market and sell a call
spread above it. The defining rule is a credit condition: **if the total credit collected is greater
than the width of the call spread, there is no risk to the upside** — even if the stock rockets, the
call spread's max loss (its width) is fully covered by the premium you took in. All your remaining
risk is to the **downside**, through the short put (assignment / a falling stock), exactly like a
cash-secured put with a bonus. It is a high-IV, neutral-to-bullish premium-selling trade for people
who are comfortable owning the stock if it drops but never want to sweat a rally. The library builds
the legs; **the analyzer checks the credit-vs-width rule** — the factory does not enforce it, so you
must verify it yourself (`net credit ≥ call-spread width`).

### When complexity is actually paid for

Every leg you add is another bid/ask spread crossed, another commission, another thing to manage, and
another way to be wrong about fills. Complexity is *paid for* only when the structure expresses a
view you genuinely hold that a simpler trade cannot — a ratio when you want a wide no-loss zone and
will accept a tail; a backspread when you truly expect a violent move and want convexity cheaply; a
BWB when you want to be paid to be wrong on one side; a jade lizard when you want premium with zero
upside risk. If a plain vertical or condor captures your view at a tighter total spread, **trade the
simpler thing.** The exotic is not more sophisticated for its own sake — it is a tool for a specific
asymmetry.

### Margin, sizing, and the naked-leg reality

Two of these structures carry an *undefined* leg — the ratio spread's extra short and the jade
lizard's short put — and that changes how you size and margin them. A defined-risk BWB or a
credit-rule-satisfying jade lizard can be sized by `analyzer.max_loss` like any spread. But a ratio
spread's `max_loss` is `±inf`, and a broker will hold **naked-option margin** on the uncovered leg
(a percentage of notional that *grows* as the position moves against you). You cannot size an
undefined-risk structure with the simple fixed-% formula; instead you size it by a **stress
scenario** — "what do I lose if the underlying gaps two expected moves into my naked side?" — and you
only trade it in an account that can margin it and a temperament that can manage it. The jade lizard
is the friendliest of the group here: its only real risk is the short put's downside, identical to a
cash-secured put, so if you would sell that put anyway, the added call spread is "free" income once
the credit rule holds. The lesson: the payoff diagram is only half the picture — always check what
the *broker* thinks the risk is, because that is the capital you actually commit.

---

## Strategy cards

### Call / put ratio spread (1×2)

**Construction.** Call ratio: long 1 lower-strike call, short 2 higher-strike calls, same expiry.
Put ratio: long 1 higher-strike put, short 2 lower-strike puts. Typically entered for a small debit,
even money, or a credit. DEMO example: long 100 call (45 DTE, 3.91), short two 105 calls (45 DTE,
1.85 each = 3.70 credit) → net debit 0.21 (`$21`).

**Payoff & greeks profile.** Rising into the short strike (best case is the stock pinning the short
strike at expiry — the long is deep ITM, both shorts expire worthless-ish), then falling and going
**unbounded** past the short strike (call) or toward zero (put) because of the extra naked leg. Near
inception: mildly directional, **short vega**, **short gamma** above the shorts. The naked leg makes
it a **short-tail** trade.

**When to use it.** A target-price view: you think the stock grinds *to* a level but not far past it.
IV: prefer **elevated IV** (you are a net premium seller on the extra short). Horizon: 30–60 DTE.

**Entry criteria.** Long strike near the money or slightly ITM; short strike at your target /
resistance, chosen so the two credits roughly finance the long (aim for even-money-to-credit).
Only if you can tolerate — and margin — the naked side. Never in a name that can gap violently the
wrong way unless the naked side is puts and you would own the stock happily.

**Management & adjustment.** Take profits at 50–75% of max as the stock approaches the short strike.
If it threatens the naked side, **buy back the extra short** (converting to a plain vertical), roll
the tested short out/away, or close. Do not let the tail run.

**Exit rules.** Close at target profit, or the moment the naked side is breached and the thesis is
dead. These are not "let it ride to expiry" trades near the short strike — pin risk plus a naked leg
is a bad combination.

**Common mistakes.** Forgetting the extra leg is **naked** and sizing to the debit instead of the
tail. Putting a call ratio on a momentum name that gaps up. Ignoring margin on the short side.

### Call / put backspread (1×2)

**Construction.** Call backspread: short 1 lower-strike call, long 2 higher-strike calls. Put
backspread: short 1 higher-strike put, long 2 lower-strike puts. Often near even money or a small
debit. It is a ratio spread **reversed** — you are net long options.

**Payoff & greeks profile.** A **valley**: max (defined) loss in the zone between the strikes where
the short is ITM and the longs lag; then convex, large, and effectively unbounded profit on a big
move in the long direction. **Long gamma, long vega, long tail.** Time decay is the enemy — it bleeds
if nothing happens.

**When to use it.** You expect a **large, fast move** (breakout, event you think is under-priced) and
want cheap convexity. IV: enter when IV is **low/cheap** (you are net long options; you do not want to
overpay for vega). Horizon: enough time for the move to happen — 30–60 DTE — but respect the theta
bleed.

**Entry criteria.** Short strike near the money; long strikes where you expect price to travel to.
Structure for near-even-money so the max loss (the valley) is small and defined. Confirm the longs
are liquid.

**Management & adjustment.** If the move comes, take profits into the convex part; do not get greedy
past a target. If it stalls, cut before the valley/theta grind you down near expiry. You can roll the
whole thing out if the thesis is intact but slow.

**Exit rules.** Close on the target move, or on time decay eroding the thesis, or if IV collapses and
kills your long vega.

**Common mistakes.** Buying backspreads in **high IV** (overpaying for the longs → vol crush hurts).
Holding into expiry through the valley. Expecting a slow drift to pay — it will not; you need
violence.

### Broken-wing butterfly (BWB)

**Construction.** +1 / −2 / +1 in one option type with **unequal wings**
(`broken_wing_butterfly("call"|"put", low, mid, high, ...)`). Widen the far wing to cut its cost —
often producing a **net credit** and no risk on the near side. DEMO put BWB example: +1 92.5 put,
−2 97.5 put, +1 100 put — the wider 97.5→92.5 lower span vs 100→97.5 upper is where the risk sits.

**Payoff & greeks profile.** A butterfly tent skewed off-center, with **one side flat at the credit
(no risk)** and the other side carrying the defined max loss over the wide-wing gap. Typically a
small net credit or debit; **short vega** near the body. Peak profit at the body (mid) strike.

**When to use it.** Neutral-to-slightly-directional with a strong feeling about which way you are
*not* worried. IV: elevated (you are net short premium at the body). Horizon: 30–45 DTE.

**Entry criteria.** Body at your expected pin; break the wing on the side you are least worried about
so that side becomes riskless; verify with the analyzer that `max_loss` sits only on the wide-wing
side and that you took a credit (or an acceptably small debit).

**Management & adjustment.** Manage like a fly: take profit at 25–50% of max; if the stock runs to
the risk side, close or roll. The riskless side needs no defense — that is the point.

**Exit rules.** Profit target, or thesis break toward the risk side.

**Common mistakes.** Breaking the wing toward the side you are *actually* worried about (risk in the
wrong place). Thinking "credit = free money" and ignoring the defined loss on the wide side.

### Jade lizard

**Construction.** Short put + short call spread, same expiry
(`jade_lizard(short_put, short_call, long_call)`), with put strike < short call strike < long call
strike. **Credit rule:** total credit collected should **exceed the call-spread width** so upside
risk is zero. DEMO example: short 95 put (45 DTE, 1.58), short 105 call (1.85), long 110 call (0.73)
→ credit = 1.58 + 1.85 − 0.73 = 2.70; call-spread width = 5. Here 2.70 < 5, so **this one still has
upside risk** — you would tighten the call spread or widen the credit to satisfy the rule.

**Payoff & greeks profile.** Flat profit (the full credit) across a wide upper range **if the credit
rule holds** — no upside risk at all. Downside risk through the short put, like a cash-secured put:
losses grow as the stock falls below the put strike (net of credit). **Short vega, short gamma**,
neutral-to-bullish delta.

**When to use it.** High IV, neutral-to-bullish, and you are **willing to own the stock** if it drops
to the put strike. IV: high IV rank is close to a requirement (you are a net premium seller). Horizon:
30–45 DTE.

**Entry criteria.** Sell the put at a strike you would happily buy stock at (~16–30Δ). Sell the call
spread above resistance; size the call-spread **width ≤ total credit** so upside risk is eliminated —
this is the defining check, done in the analyzer, *not* by the factory.

**Management & adjustment.** Defend the put side like a cash-secured put / bull put spread: roll the
put down and out for a credit if tested, or take assignment if you wanted the shares. The call spread
rarely needs attention if the credit rule holds.

**Exit rules.** Take profit at ~50% of the credit; manage the short put on a breach.

**Common mistakes.** **Violating the credit rule** (credit < call-spread width) and unknowingly
carrying upside risk. Selling the put at a strike you would *not* want to own. Treating the downside
as defined — it is not; the short put's risk runs toward zero.

---

## Key takeaways

- These structures **relocate** risk, they do not remove it — always find where the tail or the
  defined max loss now sits.
- **Ratio spreads** finance a wide no-loss zone with a **naked** leg (unbounded/short-to-zero tail);
  high-IV, target-price trades.
- **Backspreads** pay a little for **net-long convexity** and a big move; low-IV, long-vega,
  long-tail — they bleed if nothing happens.
- **Broken-wing butterflies** widen one wing to erase risk on one side (often for a credit); the
  wide-wing side carries the defined loss.
- **Jade lizards** have **no upside risk only if credit ≥ call-spread width** — verify it in the
  analyzer; all remaining risk is the short put's downside.
- Add complexity **only** when it expresses a view a simpler vertical/condor cannot at a tighter
  total spread.

## In the next module

We stop cataloguing structures and start *choosing* them: the strategy selection matrix — direction
× IV level × horizon → the right structure — plus the regime and event awareness that decides which
row of the matrix you are even in.
