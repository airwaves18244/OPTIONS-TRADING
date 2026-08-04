# 08 — Exercises: Ten Scenario Drills (Exit Gate 3)

These ten drills **are** exit gate 3. For each: (a) pick a structure, (b) justify it in the matrix's
terms — direction × IV level × horizon, (c) state entry criteria (strikes/DTE/liquidity), and (d)
state the exit/adjustment plan **before** you would open it. Your structure may differ from the key;
your *reasoning* must hold. Where a chain is named, build your pick in the notebook and confirm the
numbers fit the thesis.

Work all ten without the key. Then compare.

---

**Drill 1.** DEMO (spot 100). IV rank 12. You are moderately bullish over ~60 days; you think it
grinds toward 110 but not far past. Pick and defend.

**Drill 2.** HIGHVOL (spot 62). IV rank 78. Neutral — you expect it to chop between 55 and 70 for
the next month. Earnings are **not** until after your expiry. Pick and defend.

**Drill 3.** LOWVOL (spot 185). IV rank 20. You are convinced a pending product announcement in ~3
weeks causes a large move but you have **no idea which direction**. Pick and defend.

**Drill 4.** DEMO (spot 100). IV rank 65. Mildly bearish over 45 days; you would be fine being short
stock at 105 and you want to be paid. Pick and defend.

**Drill 5.** HIGHVOL (spot 62). IV rank 80. Bullish; you would genuinely like to own shares at 55 and
you never want to worry about the upside. 30-day horizon. Pick and defend.

**Drill 6.** LOWVOL (spot 185). IV rank 18. Strongly bullish with conviction over 90 days, but you
have limited capital and do not want to tie up `$18,500` in shares for a covered-call-style income
trade. Pick and defend.

**Drill 7.** DEMO (spot 100). IV rank 55. Neutral-to-slightly-bullish; you expect a pin near 100–102
into a known event in 25 days, and you think front-month IV is rich relative to the back. Pick and
defend.

**Drill 8.** HIGHVOL (spot 62). IV rank 30 (middling-low for this name). Bearish with real conviction
over 45 days — you think it breaks down hard. Pick and defend.

**Drill 9.** DEMO (spot 100). IV rank 70. Neutral, but you are in a **small account** that cannot
carry undefined risk, and the underlying is only moderately liquid (2.5-wide strikes, thin far
wings). 40-day horizon. Pick and defend, and name the tie-breaker that decides.

**Drill 10.** LOWVOL (spot 185). The market has been in a clear **uptrend** (rising 50-day average,
higher lows); IV rank 25. You are trend-following bullish over ~45 days and want defined risk with a
credit if possible. Pick and defend, and note how the *regime* read changes the answer versus a
ranging market.

---

## Answer key

**Drill 1 — Low IV, bullish, target-price.** Buy premium / debit. Best fit: **bull call debit
spread** (e.g., long 100 call / short 110 call, 45–60 DTE) — defined risk, cheap in low IV, capped at
your 110 target (you do not expect much past it). Alternative: a **call diagonal** if you want to sell
the front repeatedly. Entry: long ATM-ish, short at the 110 target, both liquid. Exit/adjust: take
~50–75% of max; roll up the short if it rallies through 110 with room left; cut if the bullish thesis
breaks. Why not a credit spread? In *low* IV you want to be a net buyer — the column decides.

**Drill 2 — High IV, neutral, ranging, no event.** Sell premium. Best fit: **iron condor** (short
~55 put / ~70 call spreads, 30 DTE) — defined risk, wide profit zone matching the 55–70 range, no
event to gap it. Alternatives: short strangle (higher credit/POP but undefined — only if the account
tolerates it) or iron butterfly (if you expect a tighter pin). Entry: shorts near the range edges
(~16Δ), long wings 2.5–5 wide, confirm liquidity. Exit/adjust: 50% profit target or 21 DTE; roll the
untested side in for more credit if one side is tested; go inverted / convert to a fly if breached.

**Drill 3 — Low IV, big move, direction unknown.** Long vol. Best fit: **long strangle** (or straddle)
in the ~21-day cycle covering the announcement — cheap in low IV, profits from a large move either
way. Backspread only if you actually lean one way. Entry: strikes bracketing spot (straddle ATM;
strangle ~1 expected-move wide), enough time to include the event, liquid. Exit/adjust: take profits
into the post-event move / vol pop; cut quickly if the event passes with a small move (theta + vol
crush will bleed it). Note: buying vol *before* the event means you also benefit from the IV ramp.

**Drill 4 — High IV, mildly bearish, willing to be short at 105, wants to be paid.** Sell premium,
bear side. Best fit: **bear call credit spread** (short 105 call / long 110 call, 45 DTE) — defined
risk, collects rich IV, profits if DEMO stays below 105. "Willing to be short at 105" also permits a
naked short call, but defined risk is the disciplined choice. Entry: short ~30Δ call at/above 105,
long wing above, liquid. Exit/adjust: 50% target; roll up-and-out for a credit if tested; the untested
downside needs no defense.

**Drill 5 — High IV, bullish, happy to own at 55, no upside worry.** Best fit: **jade lizard** (short
55 put + short call spread above, 30 DTE) — the "no upside worry" plus "happy to own at 55" is exactly
the jade lizard's shape, provided **credit ≥ call-spread width** (verify in the analyzer; tighten the
call spread if needed). Alternative: cash-secured put if you drop the call-spread income. Entry: sell
the 55 put (~16–30Δ), sell a narrow call spread far enough OTM that credit covers its width. Exit:
50% of credit; defend the put like a CSP (roll down-and-out or take assignment).

**Drill 6 — Low IV, strongly bullish, capital-constrained, income tilt.** Best fit: **poor man's
covered call (PMCC)** — a deep-ITM long-dated call (90–180 DTE, delta ≥ ~0.75) as synthetic stock,
short a near OTM call against it. Delivers covered-call-style income for a fraction of the `$18,500`.
Alternative in low IV with strong conviction: a long-dated debit call spread. Entry: long call deep
ITM with small extrinsic; short ~30Δ call 21–30 DTE, strike **above** the long strike; check the
width+credit vs debit so max upside is a profit. Exit/adjust: roll the short call out/up for credit
each cycle; roll the long out before its final weeks.

**Drill 7 — Middling-high IV, neutral pin into an event, front IV rich vs back.** Best fit:
**calendar spread** at the ~100 strike (short the 21-DTE front whose IV is rich, long a ~45-DTE back)
— sells the elevated front vol, long back-month vega, tent peaks at the pin. Alternative: a long
butterfly if you have no vol view. Entry: strike at the 100–102 pin target; front just inside the
event framing, back further out; **know exactly where the event sits relative to both expiries**.
Exit/adjust: manage at/near front expiry (mark-to-model with `pnl_at`), take ~20–30%; roll the strike
if it drifts. Do not hold through front-expiry gamma.

**Drill 8 — Low-ish IV, bearish conviction, expects a hard break.** Buy premium / convexity. Best
fit: **bear put debit spread** (long 100 put / short 90 put, 45 DTE) for defined-risk directional
downside, or a **put backspread** (short 1 higher / long 2 lower) if you want convex payoff on a
violent drop and can stomach the valley. Both suit *low* IV (net long options). Entry: long ATM/ITM
put, short at the downside target; backspread structured near even money. Exit/adjust: take profits
into the break; cut if it stalls (theta). Why not a bear *call* credit spread? IV is not high enough
to prefer selling, and you have conviction for a move — buy the convexity.

**Drill 9 — High IV, neutral, small account, thin liquidity.** Best fit: **iron condor or iron
butterfly** — *defined risk is mandatory* in a small account (no naked strangle). The deciding
tie-breaker is **liquidity + account size**: thin far wings and 2.5-wide strikes argue for a
**narrower iron butterfly or a tight condor** (fewer/closer strikes, less slippage) over a wide condor
whose distant wings you cannot fill well. Entry: keep wings where markets are penny-ish; size by max
loss to a small % of the account. Exit/adjust: 50% / 21 DTE; roll untested side; the veto here is
that liquidity and buying power outrank the "ideal" wide condor.

**Drill 10 — Low IV, trending up, wants defined risk + credit.** Best fit: **bull put credit spread**
placed under support / below the trend (short ~30Δ put / long wing below, 45 DTE) — in an **uptrend**,
selling downside puts aligns with the trend and collects a credit; defined risk. Note the regime
dependence: in a **ranging** market you would instead lean neutral (condor) or use a debit call spread
for the low-IV bullish view — but the trend read tilts you to *sell the downside* rather than fade the
move. IV rank 25 is low, so the credit is thinner than in high IV; keep size modest and consider a
debit call spread as the pure low-IV alternative if the credit is too skimpy. Exit/adjust: 50% target;
roll down-and-out for credit if the trend stalls and the short put is tested; exit if the trend breaks
(thesis gone).

**Scoring yourself.** You pass if, for at least 8 of 10, you (1) picked the correct IV *column*
(buyer vs seller), (2) matched the structure to direction and horizon, (3) gave concrete entry
criteria, and (4) stated an exit/adjustment plan before entry. Picking a reasonable alternative
structure is fine; mismatching the IV column (e.g., buying premium in high IV) or having no
management plan is a fail — redo those drills.
