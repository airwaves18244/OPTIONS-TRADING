# 07 — Exercises: Advanced Structures

Use the DEMO chain (spot 100) at 45 DTE unless told otherwise. Mids you will need:
100 call 3.91, 105 call 1.85, 110 call 0.73, 95 put 1.58, 92.5 put 1.01, 97.5 put 2.37,
100 put 3.42, 90 put 0.62. Verify with `optionslab`.

---

**1. (Calculation) Call ratio net premium.** Build a 1×2 call ratio: long one 100 call (3.91), short
two 105 calls (1.85 each). What is the net premium in dollars, debit or credit? Which leg is naked,
and in which direction is the tail risk unbounded?

**2. (Calculation) Ratio no-loss zone.** For that ratio, use `analyzer.max_loss` and
`analyzer.max_profit`. Where is max profit located (which spot), and what does `max_loss` return —
is it a finite number or `-inf`? Explain the sign.

**3. (Concept) Ratio vs backspread.** Without building it, state how a 1×2 call **backspread** (short
one 100 call, long two 105 calls) differs from the ratio in Exercise 1 in: net option position
(long/short), gamma sign, vega sign, and which IV environment you want at entry.

**4. (Calculation) Backspread valley.** Build the call backspread (short 100 @ 3.91, long two 105 @
1.85). Net premium? Use `payoff.pnl_curve` at expiry across spots 95–120 and identify the spot of
maximum loss (the valley bottom). Why is the loss defined here but unbounded in the ratio?

**5. (Calculation) Broken-wing butterfly.** Build a put BWB: `broken_wing_butterfly("put",
low=(92.5, 1.01), mid=(97.5, 2.37), high=(100.0, 3.42))` (+1 / −2 / +1). Report `net_premium`,
`max_profit`, and `max_loss` from `analyzer.summarize`. Which side (up or down) is the riskless side,
and which wing carries the defined loss?

**6. (Calculation) Jade lizard credit rule.** Build the jade lizard: short 95 put (1.58), short 105
call (1.85), long 110 call (0.73). Compute total credit and the call-spread width. Does the credit
rule (credit ≥ width) hold? Does this structure have upside risk? If yes, propose one concrete change
to eliminate it.

**7. (Scenario judgment) Pick the structure.** You are neutral-to-slightly-bullish on DEMO, IV rank
is high (~70), you would be happy to own DEMO at 95, and you never want to worry about a rally.
45-day horizon. Which of this module's structures fits best, and what one check must you run before
sending it?

**8. (Break it) Find the flaw.** "IV rank is 15 (very low). I'm putting on a 1×2 call ratio for a
credit because I love free premium, and I'll hold to expiry to collect the whole thing." List at
least three problems.

---

## Answer key

**1.** Net premium = (long 3.91 − 2 × 1.85) × 100 = (3.91 − 3.70) × 100 = **+$21 debit** (very close
to even money). The **extra second 105 call is naked**; tail risk is **unbounded to the upside** —
above 105 you are effectively short one call with no cover, and losses grow without limit as the
stock rises.

**2.** **Max profit is at the short strike, spot ≈ 105** at expiry: the long 100 call is worth 5 of
intrinsic, both 105 calls expire ~worthless, so payoff ≈ `$500` minus the `$21` debit ≈ `$479`.
`analyzer.max_loss` returns **`-inf`**: the naked upper leg makes the loss unbounded, which the
analyzer detects from the negative P&L slope at the top of the grid. (Downside is limited to the
`$21` debit, but the reported max loss is the worst case, which is the infinite upside tail.)

**3.** The backspread is **net long options** (long 2, short 1) versus the ratio's net short. Gamma:
backspread **long gamma** (ratio short gamma). Vega: backspread **long vega** (ratio short vega). IV
at entry: you want **low/cheap IV** for the backspread (you are buying net premium) versus **elevated
IV** for the ratio (you are net selling). They are mirror trades built from the same three-strike
skeleton.

**4.** Net premium = (short 3.91 credit, long 2 × 1.85 debit) = (−3.91 + 3.70) × 100 = **−$21**, i.e.
a **$21 credit**. The valley bottom sits at the **long strike, spot ≈ 105**: there the short 100 call
is 5 ITM (−`$500`) while the two long 105 calls are worthless, for the maximum (defined) loss ≈
`$500 − $21` ≈ `$479` loss. It is defined because above 105 the **two** longs overpower the one short
and the payoff turns convex/up; the ratio was undefined because it had the naked short on top instead.

**5.** From `summarize`: `net_premium` is a small **credit** (the wider lower wing cheapens the
structure; exact value from the notebook), `max_profit` at the body strike 97.5, `max_loss` finite.
Because the wings are broken with the **wider gap on the lower side** (97.5 down to 92.5 is the −2/+1
lower span), the **downside carries the defined loss** and the **upside is the riskless side** (above
100 all puts expire worthless and you keep the credit). Confirm by checking that `pnl_at_expiry` is
flat and positive for large spots and dips to `max_loss` on the downside.

**6.** Total credit = 1.58 + 1.85 − 0.73 = **1.70** (`$170`). Call-spread width = 110 − 105 = **5**
(`$500`). Credit rule credit ≥ width: **1.70 < 5 → fails**, so this jade lizard **does have upside
risk** (max upside loss ≈ width − credit = 5 − 1.70 = 3.30 → `$330`). To eliminate it, either
**tighten the call spread** to a width ≤ 1.70 (e.g., sell 105 / buy 106.5-ish, but the sample chain
is in 2.5 increments, so sell 107.5 / buy 110 is still width 2.5 > credit — you would need more
credit) or **collect more credit** by selling a closer/richer put or a closer call. The teaching
point: the factory will happily build a lizard that violates the rule; **you** must check it.

**7.** A **jade lizard**: high IV rank favors net premium selling, neutral-to-bullish fits, you are
happy to own at 95 (the short put strike), and "never worry about a rally" is exactly the
no-upside-risk feature. The one required check: **credit ≥ call-spread width**, verified in the
analyzer — size the call spread narrow enough (or collect enough put/call credit) that upside risk is
truly zero before sending.

**8.** Flaws: (a) **IV rank 15 is the wrong environment** for a ratio — a ratio is a net premium-sell
that wants *high* IV; in low IV you are selling cheap options and the naked tail is poorly
compensated. (b) **"Free premium" ignores the naked, unbounded tail** — a credit ratio still has
`-inf` max loss to the upside; the credit is tiny relative to the risk. (c) **Holding to expiry** sits
you in pin risk *plus* a naked leg right where gamma is most violent — the worst place to be. (d) A
low-IV directional bet is better expressed by a **backspread** (long convexity, cheap when IV is low)
or a simple long/vertical, not by selling a naked ratio. Better plan: if you must sell premium, wait
for high IV; if you expect a move in low IV, buy convexity instead.
