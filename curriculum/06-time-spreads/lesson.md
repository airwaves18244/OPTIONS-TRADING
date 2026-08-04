# 06 — Time Spreads: Trading the Calendar

Every structure you have built so far shares one expiration date. All the legs live and die
together, so the only thing that moves your P&L is where the underlying lands relative to your
strikes. This module breaks that assumption. When two legs expire on **different** dates, you are
no longer trading only *direction* — you are trading **time itself**, and the *shape* of implied
volatility across expirations. After this module you can build a calendar, a diagonal, and a poor
man's covered call; explain why each one wants a specific term-structure and price path; and, most
importantly, you can value them correctly, because a naive "everything at intrinsic" expiry diagram
is *wrong* for these trades and will lie to you about your risk.

---

## Concepts / Mechanics

### The two things a time spread trades

A time spread (also called a **horizontal** or **calendar** spread) is short one expiration and
long another at related strikes. Two forces drive it:

1. **Differential theta (time decay).** Extrinsic value bleeds out of an option faster as expiry
   approaches — decay accelerates in the final weeks and is roughly proportional to `1/sqrt(t)`.
   The **front** (near-dated) option you are short therefore decays *faster* than the **back**
   (far-dated) option you are long. If the underlying sits still, you collect that decay
   differential. A time spread is fundamentally a **long-theta** position (when structured
   short-front / long-back).

2. **Term structure of implied volatility.** The front and back options usually carry *different*
   IVs. The relationship of near-dated IV to far-dated IV is the **term structure**. Normally it
   is upward-sloping (**contango**): far-dated IV > near-dated IV, because more time means more
   uncertainty. Before an event — earnings, an FDA decision, a Fed meeting — the front month gets
   bid up and term structure **inverts** (**backwardation**): near-dated IV > far-dated IV. A
   calendar is **long vega** on net (the back option has more vega than the front), so it wants
   *rising* or *stable* vol, and it profits when an inverted front-month IV collapses after the
   event ("**vol crush**") while your longer-dated leg holds its value.

Put those together and the ideal calendar environment is: **underlying pins near your strike,
front-month IV is elevated relative to back-month, and you expect that front premium to bleed or
crush while your back leg survives.**

### Why the expiry diagram lies (read this twice)

For a same-expiry vertical, `payoff.payoff_at_expiry` is exact: at expiry every option is worth its
intrinsic value, full stop. For a **mixed-expiry** position it is a lie. When the front leg expires,
the back leg is *still alive* and still carries **extrinsic value** — it is not worth intrinsic yet.
The library's docstring says this outright: `payoff_at_expiry` treats "all legs at intrinsic" as a
simplification, and for calendars/diagonals you must instead use `payoff.pnl_at` evaluated at the
**front leg's expiry**. That function re-prices every surviving leg with Black-Scholes at its
*remaining* time to expiry, so the back option is valued as the live instrument it actually is.

Concretely: a calendar's real P&L picture is the curve produced by
`payoff.pnl_curve(pos, spots, t_elapsed=front_dte/365, vol=...)`. That is the tent-shaped profit
diagram you have seen for calendars — and it exists *only* in mark-to-model space. The intrinsic
diagram would show a meaningless V or flat line. **Rule: any position whose legs have different
expiries is analyzed with `pnl_at` / `pnl_curve` at `t_elapsed`, never with the plain expiry
payoff.** This is the single most important mechanical idea in the module and the reason the
analyzer exists.

### Earnings and the calendar

Term structure is most tradeable around scheduled events. Say DEMO reports earnings in 25 days. The
front-month (21-DTE, expiring *before* earnings would be one choice; or the cycle capturing
earnings) carries event premium. A calendar that is **short the expiration that contains the event
and long a later one** is a way to sell rich event vol while staying defined-risk — but be careful:
if you are short the front and the event lands *inside* the front's life, a big gap can blow through
your tent. The cleaner "sell the crush" calendar is short the *post-event* elevated front and long
further out, or simply short a front whose IV is inflated relative to the back with no binary event
in between. Always know **where the earnings date sits relative to both expiries.**

You can see term structure directly in the DEMO chain. At the 100 strike, the 21-DTE call carries IV
0.2658 while the 45-DTE carries 0.2621 — the near month is *richer* than the far, a mild inversion.
That small backwardation is exactly the tailwind a long calendar wants: you are selling the
0.2658 front and buying the 0.2621 back, collecting the relatively expensive near-term vol. Contrast
that with a name in steep contango (front much cheaper than back) — there a calendar is paying up for
the wrong side of the curve, and you would want a diagonal or a different structure instead. Reading
the front-vs-back IV before you build the calendar is not optional; it is the difference between a
tailwind and a headwind.

### The vol-crush trap (and why calendars are two-sided vol bets)

Because a calendar is net long vega, it *wants* vol — but it is not immune to a crush. The nuance is
*which* leg the crush hits. A calendar profits when the **front** IV falls faster than the **back**
(the front decays and, post-event, crushes hard while the longer-dated back holds its value). It
*loses* on a **broad, parallel vol collapse** that drags the back leg down too, because you own more
vega in the back. So the ideal setup is a *term-structure* trade — inverted or steep front-month vol
that normalizes — not a bet on the whole vol surface rising. This is why the sample calendar's
scenario grid across vols (in the notebook) is worth studying: a +3-vol shift helps, but a crush that
hits both months can turn the tent into a loss even if the stock pins your strike. When you put on a
calendar, ask: *what specifically do I expect to crush — the front only, or everything?* If it is
"everything," you do not want a calendar.

### Managing the mixed-expiry clock

One practical wrinkle of mixed expiries: your position's character *changes* as the front leg
approaches expiry. A calendar that was comfortably delta-neutral and long theta at entry becomes
increasingly **short gamma** right around the strike in the front leg's final days — the same pin
dynamic that makes near-expiry short options dangerous. Combined with the fact that the tent's peak
value occurs *at* front expiry, this means calendars and diagonals are actively-managed trades: you
harvest most of the value in the days before the front expires and you rarely want to be sitting on
the front strike into its last session. Set a calendar reminder for the front expiry the day you open
the trade.

---

## Strategy cards

### Calendar spread (horizontal)

**Construction.** Same strike and same kind (both calls or both puts). Sell the front-month option,
buy the back-month option. Net **debit** (the longer option costs more). Example on DEMO (spot 100):
sell the 100 call at 21 DTE for 2.66, buy the 100 call at 45 DTE for 3.91 → net debit 1.25
(`$125` per spread). ATM calendars are the standard; the strike is where you want the stock to pin.

**Payoff & greeks profile.** Tent-shaped in mark-to-model space: maximum value when the underlying
sits *at the strike* at front expiry (front option expires worthless, back retains maximum
extrinsic). Losses on both sides as the stock moves away and both options converge to the same
intrinsic. **Long theta** (you earn the front's faster decay), **long vega** (back has more vega
than front), roughly **delta-neutral** at inception for an ATM calendar, **short gamma** near the
front strike as front expiry approaches.

**When to use it.** Neutral-to-pin view: you expect the underlying to *stay near the strike*
through front expiry. IV environment: you want front IV **not** cheap relative to back — ideally
front elevated (term structure flat or inverted), because you are net long back-month vega and you
sell the richer front. Horizon: front leg 2–5 weeks, back leg roughly double.

**Entry criteria.** Choose the strike at your pin target (ATM for neutral, slightly OTM to add a
directional lean). Front DTE ~21–30, back DTE ~45–60. Confirm both legs are liquid (tight
bid/ask, real open interest). Prefer entering when front-month IV is at or above back-month IV.

**Management & adjustment.** Profit target ~20–30% of the debit is typical; these are not
"hold to expiry" trades because the tent is tallest *right at* front expiry only if the stock
pinned. If the underlying drifts toward one edge, you can **roll the strike** (close and re-open the
calendar centered on the new price) or **roll the short leg out** to collect more premium and extend
the trade into a longer diagonal. Take it off before front-expiry gamma gets violent if the stock is
near your strike and you do not want pin risk.

**Exit rules.** Close at the profit target, or when front-month IV has crushed and the edge is gone,
or if the stock moves beyond your break-evens and the thesis (pin near strike) is dead. Do not carry
a calendar through the front expiration hoping — manage it before.

**Common mistakes.** Reading the intrinsic expiry diagram instead of the `pnl_at` curve.
Buying a calendar when front IV is *below* back IV (you are paying up for the wrong term structure).
Ignoring an earnings date sitting between the two expiries. Sizing it like a defined-risk condor
and forgetting that a fast directional move loses the whole debit.

### Diagonal spread

**Construction.** Like a calendar but with **different strikes** as well as different expiries: sell
a nearer-dated option at one strike, buy a farther-dated option at another. Direction comes from the
strike offset. A **call diagonal** (buy a lower-strike back call, sell a higher-strike front call)
is a bullish, long-theta, defined-ish-risk trade — essentially a calendar with a directional tilt,
or a "financed" long call. Net debit, usually smaller than the equivalent long call because the
short front leg subsidizes it.

**Payoff & greeks profile.** An asymmetric tent, skewed toward the direction of your long strike.
Long theta and long vega like a calendar, but with a directional delta because the strikes differ.
The back-month long strike sets your upside participation; the front short strike is where you sell
decay.

**When to use it.** A *directional-but-patient* view: mildly bullish (call diagonal) or bearish (put
diagonal), willing to let time and a stable-to-rising vol work for you. IV: same logic as the
calendar — you want to be net selling the richer front. Horizon: weeks to a couple months.

**Entry criteria.** Back leg 45–90 DTE at a strike near or slightly ITM in your direction; front leg
~21–30 DTE at an OTM strike you would be happy to see the stock reach. Keep the width modest so the
short leg meaningfully finances the long.

**Management & adjustment.** The signature move: **roll the short front leg** forward each cycle,
collecting fresh premium and grinding your cost basis down — the same mechanic as a covered call,
which is exactly what the PMCC formalizes. Roll up the short strike if the stock rallies and you want
more room; roll down for more credit if it stalls.

**Exit rules.** Close when the back leg's directional thesis is realized, when repeated short-leg
rolls have recovered your debit (house money), or when the thesis breaks.

**Common mistakes.** Setting the short strike so close that a rally caps you immediately for little
credit. Forgetting the back leg still has vega risk if IV collapses. Letting the short leg go ITM
into expiration and getting assigned unexpectedly.

### Poor man's covered call (PMCC)

**Construction.** A capital-efficient stand-in for a covered call. Instead of buying 100 shares, buy
a **deep-ITM long-dated call** (a LEAPS-style call, high delta ~0.75–0.85, acting as your synthetic
stock) and sell a **near-dated OTM call** against it. The factory:
`poor_mans_covered_call(long_call=(strike, premium), short_call=(strike, premium), long_expiry=...,
short_expiry=...)`, requiring `short_expiry < long_expiry` and long strike < short strike.

**Payoff & greeks profile.** Mimics a covered call's capped-upside / cushioned-downside shape but
for a fraction of the capital. **Long delta** (from the deep-ITM call, but less than 100 shares'
worth), **long theta** on net once the short call's decay dominates, **long vega** (net long a
longer-dated option). Max profit near the short strike at front expiry; the deep-ITM long defines
your downside (you can lose the long call's value, unlike owning stock that could go to zero — but
also unlike stock, the long call decays).

**When to use it.** Moderately bullish, income-oriented, capital-constrained. You want covered-call
cash flow without tying up `$18,500` in DEMO shares. IV: neutral-to-high is fine; you are selling
the front repeatedly. Horizon: months (the long call), rolling the short weekly-to-monthly.

**Entry criteria.** Long call: 60–180+ DTE (in this curriculum's samples, use the longest available,
e.g. 180 DTE), strike deep enough ITM that delta ≥ ~0.75 and extrinsic is small (you do not want to
bleed theta on the leg you are holding). Short call: ~21–30 DTE, OTM, strike above your long strike,
delta ~0.30. **Critical width rule:** the difference between the two strikes plus the net credits you
expect to collect should comfortably exceed the debit paid, or the upside can turn into a loss — check
it with the analyzer.

**Management & adjustment.** Roll the short call out (and up, if the stock rallies) each cycle for a
credit, exactly like a covered call. Reduce cost basis over time. If the stock tanks, the long call
loses value but far less in dollars than 100 shares would; you can roll the short call *down* for
more credit to defend.

**Exit rules.** Close when the long call's runway shortens (don't hold a LEAPS into its own final
weeks — roll it out earlier), when the thesis breaks, or when accumulated short-call credits plus
intrinsic have delivered your target.

**Common mistakes.** Buying a long call that is not deep enough ITM (too much extrinsic → you bleed
theta on your "stock"). Selling a short strike *below* your long strike (you can lock in a loss on a
big rally). Forgetting the long call has an expiry and letting it rot. Treating it as riskless — a
gap down still hurts.

---

## Key takeaways

- Time spreads trade **theta differential** and **vol term structure**, not just direction.
- Short-front / long-back structures are **long theta** and **long vega**; they want the underlying
  to sit near the strike and front-month vol to hold up or crush post-event.
- **Never** analyze a mixed-expiry position with the plain intrinsic expiry diagram. Use
  `payoff.pnl_at` / `pnl_curve` at `t_elapsed = front_dte/365`; that tent is the real picture.
- A **calendar** is neutral/pin; a **diagonal** adds a directional lean via a strike offset; a
  **PMCC** is a capital-efficient covered call (deep-ITM LEAPS + rolled short calls).
- Always locate the **earnings/event date** relative to *both* expiries before putting one on.
- Manage before front expiry — pin-risk gamma near the short strike gets violent in the last days.

## In the next module

We keep shaping risk asymmetrically: ratio spreads, backspreads, broken-wing butterflies, and the
jade lizard — structures that deliberately make one side of the payoff cheaper or riskless than the
other, and the question of when that extra complexity actually pays.
