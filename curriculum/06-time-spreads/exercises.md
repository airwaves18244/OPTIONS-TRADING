# 06 — Exercises: Time Spreads

Work these without the key. Use the DEMO chain (spot 100) unless told otherwise. Prices below are
mids from `data.load_sample_chain("DEMO")`. Verify numeric answers with `optionslab`.

Reference DEMO call mids (strike @ DTE): 100@21 = 2.66, 100@45 = 3.91, 105@21 = 0.84,
100@180 = ~ (deep-value; compute), 82.5@180 (deep ITM). Reference put mids: 100@21 = 2.43,
100@45 = 3.42.

---

**1. (Calculation) Build the ATM calendar.** Sell the DEMO 100 call at 21 DTE (2.66), buy the DEMO
100 call at 45 DTE (3.91). What is the net premium in dollars, and is it a debit or credit? Which
leg carries more vega, and what does that make the position's net vega sign?

**2. (Concept) Why not the expiry diagram?** A classmate plots this calendar with
`payoff.payoff_at_expiry` across spots and gets a jagged line that dips to a loss right at 100.
Explain in two sentences why that diagram is wrong and exactly what call replaces it.

**3. (Calculation) The tent's peak.** Using `payoff.pnl_at`, evaluate the calendar's P&L at
`t_elapsed = 21/365`, `vol = 0.26`, at spots 90, 100, and 110. Which spot gives the highest P&L, and
why does the peak sit at 100?

**4. (Scenario judgment) Term structure.** You are considering a 100 calendar. The front (21 DTE) IV
is 0.2658 and the back (45 DTE) IV is 0.2621. Is term structure in contango or backwardation here?
Does this small inversion help or hurt a *long* calendar, and would you want it larger or smaller
before entering?

**5. (Calculation) Vega sensitivity.** Use `analyzer.scenario_grid` on the calendar with
`vol_shift = [-0.03, 0.0, +0.03]` at `days_forward = [10]`, `spots = [100]`. Report the three P&L
numbers. Which direction of vol change helps the calendar, and does that match "long vega"?

**6. (Calculation) Diagonal.** Build a bullish call diagonal: buy the 100 call at 45 DTE (3.91),
sell the 105 call at 21 DTE (0.84). Net debit? Compared with just buying the 100/45 call outright,
how much did the short leg subsidize the cost, and what did you give up in exchange?

**7. (Calculation) PMCC width rule.** Build a PMCC: long the 82.5 call at 180 DTE (compute its mid
with `pricing.bsm_price` using the chain IV), short the 105 call at 21 DTE (0.84). Is the condition
"(short strike − long strike) + net credit collected > net debit paid" satisfiable, i.e., is your
max upside a profit? Use `analyzer.summarize` and report `max_profit` and `net_premium`.

**8. (Break it) Find the flaw.** "I'm putting on a 100 calendar in DEMO to sell earnings vol.
Earnings are in 30 days. I'll sell the 21-DTE 100 call and buy the 45-DTE 100 call, and I'll hold
both legs all the way to the 45-DTE expiration to collect maximum decay." List at least three things
wrong with this plan.

---

## Answer key

**1.** Net premium = (buy 3.91 − sell 2.66) × 100 = **+$125 debit** (`net_premium()` returns
`+125`, positive = debit). The **back-month (45 DTE) long call carries more vega** — vega rises with
time to expiry — so the position is **net long vega**. It is also net long theta because the front
decays faster than the back.

**2.** The expiry diagram assumes *every* leg is worth intrinsic, but when the front (21 DTE) call
expires the back (45 DTE) call is still alive and still holds extrinsic value, so valuing it at
intrinsic understates it and produces a false loss at the strike. Replace it with
`payoff.pnl_at(pos, spot, t_elapsed=21/365, vol=...)` (or `pnl_curve` at that `t_elapsed`), which
re-prices the surviving back leg with BSM at its remaining 24 days.

**3.** Spot **100** gives the highest P&L. At front expiry with the stock at 100, the short front
call expires worthless (you keep its full premium) while the long back call retains the most
extrinsic value of any spot — an ATM option has peak extrinsic. Move away from 100 in either
direction and the front gains intrinsic against you and/or the back loses extrinsic, so the tent
falls off on both sides.

**4.** Front IV 0.2658 > back IV 0.2621, so term structure is **inverted (backwardation)** at these
strikes. A long calendar is net short the front and net long the back, so selling a *richer* front
relative to the back **helps** — you are collecting the inflated near-term premium. You would
generally welcome a *larger* inversion before entering (more front premium to sell), provided it is
not caused by a binary event sitting inside the front's life that could gap through your tent.

**5.** Exact numbers come from the notebook, but the **+0.03 vol shift produces the highest P&L** and
**−0.03 the lowest**. Rising IV lifts the longer-dated leg (more vega) more than the front, so the
net position gains — consistent with **net long vega**. (This is why a calendar wants stable-to-rising
vol and is hurt by a broad vol crush that hits the back leg too.)

**6.** Net debit = (3.91 − 0.84) × 100 = **+$307 debit**, versus **$391** for the outright 100/45
call — the short 105 call subsidized **$84**. In exchange you **capped your upside** at/around the
105 short strike for the front cycle (a rally far past 105 by front expiry leaves gains on the table)
and took on the obligation of the short call. You also converted a pure long-vega/long-theta-negative
long call into a more theta-friendly diagonal.

**7.** Compute the 82.5/180 call: `pricing.bsm_price("call", 100, 82.5, 180/365, iv_for_82.5@180)`
— deep ITM, roughly 18–19 of intrinsic plus modest extrinsic, so a debit near `$1,900`-ish per
spread. The short 105 call adds only `$84` credit for this cycle, so on **this single cycle** the
"(105 − 82.5) + credit" width of `$2,250 + $84 = $2,334` versus the debit determines whether max
upside is green. The point of the exercise: one short-call cycle is not enough — the PMCC works
because you **roll the short call for credit repeatedly**, grinding the ~`$1,900` basis down over
many cycles. `summarize` will show `net_premium` ≈ the debit and a `max_profit` capped near the 105
strike; check that `max_profit > 0` after accounting for realistic repeated credits, and that the
long call is deep enough that its delta ≥ ~0.75.

**8.** Flaws: (a) **You cannot hold both legs to the 45-DTE expiration** — the front leg expires at
21 DTE; after that you no longer have a calendar, you have a naked long back call. (b) **"Maximum
decay" is collected at the *front* expiration, not later** — the tent is tallest at 21 DTE with the
stock near 100; there is nothing to hold for. (c) **Earnings at 30 days land *between* the two
expiries** (after the 21-DTE front, before the 45-DTE back), so the event happens while you hold only
the long back call — you are long vega into the event, not selling the crush; a gap will move the
back call unpredictably. (d) Analyzing "maximum decay at expiry" with the intrinsic diagram is the
same mixed-expiry error from Exercise 2. A better plan: size the calendar around where earnings sit,
and **manage/close near the 21-DTE front expiration**, not hold blindly.
