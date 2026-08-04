# 05 — Neutral Income: Exercises

Reason first, then verify with `strategies.*`, `analyzer.summarize`, `analyzer.expected_move`, and
`analyzer.scenario_grid`. DEMO: spot **$100**, IV **0.25**, **45 DTE**. Chain mids from module 00.

---

### 1. Expected move (calculation)
Compute DEMO's 45-DTE 1-sigma expected move with `analyzer.expected_move`. (a) What is the ~68%
range? (b) If instead IV were 0.40 (event vol), what would the expected move be? (c) Why is this
number the reference for every range trade?

### 2. Straddle breakevens and the crush (calculation/judgment)
You buy the DEMO ATM straddle (100 call 3.91 + 100 put 3.42). (a) Net debit and the two breakevens?
(b) How far (in %) must DEMO move to break even, and how does that compare to the expected move from
#1? (c) You buy it the day before earnings with IV at 0.45; the stock moves 6 points and IV crushes
to 0.25. Are you assured a profit? Name the greek that decides it.

### 3. Iron condor, fully specified (calculation)
Build the DEMO condor: long 90 put (0.62), short 95 put (1.58), short 105 call (1.85), long 110
call (0.73). (a) Net credit? (b) Max profit, max loss (per side), breakevens? (c) Where do the
breakevens sit relative to the expected-move edges from #1?

### 4. Delta-based strike selection (scenario judgment)
You want ~70% POP on a DEMO iron condor. (a) Roughly what delta short strikes target that, and
where are they on DEMO (put and call sides)? (b) If you instead sold ~30-delta shorts (95/105), how
do credit and POP change? (c) State the trade-off in one sentence.

### 5. Condor vs iron butterfly (scenario judgment)
Compare the DEMO iron condor (#3) with the iron butterfly (long 90 put, short 100 put, short 100
call, long 110 call). (a) Which collects the bigger credit and why? (b) Which has the higher
probability of reaching *max* profit? (c) When would you choose the fly over the condor?

### 6. Long butterfly economics (calculation)
Build the long call butterfly: buy 95 call (7.05), sell two 100 calls (3.91), buy 105 call (1.85).
(a) Net debit? (b) Max profit and where? (c) Max loss? (d) What is the reward-to-risk ratio, and
why does such an attractive ratio still make this a low-probability trade?

### 7. Gamma near expiry (scenario judgment)
You hold the DEMO short strangle (short 95 put / short 105 call) and DEMO is sitting at 104 with
3 days to expiration. (a) Which greek is now most dangerous, and what is its sign for you? (b) Why
does a $2 overnight move matter far more now than it did at 45 DTE? (c) What does the 21-DTE
management guideline say you should have done?

### 8. Break it (find the flaw)
A trader's income plan: "I sell the ATM short straddle on DEMO whenever I feel like it — max premium
$733 — naked, in size, and I hold to expiration to collect the full credit. IV level doesn't matter
because I'm always collecting theta." Identify at least four flaws.

---
---

## Answer key

### 1.
(a) EM = 100 × 0.25 × √(45/365) ≈ **±8.78** → ~**91.2 to 108.8**. (b) At IV 0.40: 100 × 0.40 ×
0.351 ≈ **±14.05** → ~85.9 to 114.0. (c) It is the market's own 1σ estimate of how far the stock
travels by expiration, so it tells you where to place (or judge) a range trade's breakevens —
inside the EM = more credit/less probability; outside = more probability/less credit.

### 2.
(a) Debit = 3.91 + 3.42 = 7.33 → **$733**; breakevens = 100 ± 7.33 = **92.67 / 107.33**. (b) DEMO
must move ~**7.33%** to break even, which is *less* than the ~8.78 (8.8%) expected move — so the
straddle's implied move is a touch below 1σ (a rough "is it cheap?" check). (c) **Not assured.** A
6-point move helps via delta/gamma, but you are **long vega** into a 20-point IV crush (0.45→0.25),
which deflates both legs hard; the vega loss can swamp the 6-point gain, especially since 6 < the
7.33 breakeven distance. **Vega** decides it — the classic "right on the move, killed by the crush."

### 3.
(a) Net credit = (1.58 + 1.85) − (0.62 + 0.73) = 3.43 − 1.35 = 2.08 → **$208**. (b) Max profit =
credit = **+$208** (DEMO between 95 and 105 at expiry); max loss = per-side wing width − credit =
5 − 2.08 = 2.92 → **−$292** (only one side can finish ITM, so you risk one 5-wide spread, not
both). Breakevens = 95 − 2.08 and 105 + 2.08 = **92.92 / 107.08**. (c) The breakevens
(92.92/107.08) sit **just inside** the expected-move edges (91.2/108.8) — the profit region is a bit
narrower than 1σ, consistent with the ~30-delta shorts (POP a bit under 70%).

### 4.
(a) **~16-delta** short strikes target ~68–70% POP (they sit near the 1σ / expected-move edges) —
on DEMO roughly the **90 put and 110 call**. (b) Selling ~30-delta shorts (95/105) collects a
**bigger credit** but **lower POP** (the profit zone is narrower, breakevens inside the EM). (c)
**Higher credit and higher probability trade off against each other — you pick where on that
frontier to sit.**

### 5.
(a) The **iron butterfly** collects the bigger credit (**~$598** vs the condor's ~$208) because its
short strikes are **ATM**, where extrinsic value (and thus premium) is greatest. (b) The **condor**
has the higher probability of reaching *max* profit — it keeps the full credit over the whole 95–105
range, whereas the fly's max profit requires a near-perfect pin at 100. (c) Choose the **fly** when
you have a strong **pin thesis** (you expect the stock to gravitate to a specific price) and want
the fatter credit / wider breakevens (94–106), accepting the sharper short gamma.

### 6.
(a) Debit = (7.05 + 1.85) − 2 × 3.91 = 8.90 − 7.82 = 1.08 → **$108**. (b) Max profit = wing width −
debit = 5 − 1.08 = 3.92 → **+$392**, at a pin at the **middle strike 100**. (c) Max loss = debit =
**−$108**, beyond the wings. (d) Reward:risk ≈ 392/108 ≈ **3.6:1**. It is still low-probability
because the **profit zone is narrow** (breakevens 96.08/103.92) — the market prices that great ratio
precisely because the stock rarely pins the middle strike; most flies expire at or near the small
max loss.

### 7.
(a) **Gamma** is most dangerous, and you are **short gamma** (short strangle). (b) Gamma is largest
near expiration and near the money; with DEMO at 104 (right by the 105 short call) 3 days out, a $2
move swings your delta and P&L violently and can blow past the credit collected — at 45 DTE the same
move barely moved the position. (c) The **21-DTE guideline** says you should have **taken profits
(~50% of credit) and closed/rolled the position off well before now**, rather than carrying
short-gamma risk into the final week.

### 8.
At least four flaws:
1. **Undefined risk in size.** A naked short straddle has theoretically unlimited loss; "in size"
   means one gap can exceed the account. Prefer the **defined-risk iron butterfly**.
2. **IV level absolutely matters.** Short premium is short vega — selling in *low* IV collects thin
   credit for the same (undefined) risk. "I'm always collecting theta" ignores that theta is only
   worth the gamma/vega risk when IV is *rich* (module 02).
3. **Holding to expiration maximizes short-gamma/pin risk.** Short straddles are managed at ~25% of
   credit and exited ~21 DTE precisely to avoid the final-week gamma explosion; "collect the full
   credit" is how these blow up.
4. **No loss stop and no defense plan.** An unlimited-loss trade with no stop and no roll plan is
   reckless; a tested straddle needs a defined loss trigger and a defense (roll the untested side,
   go inverted — module 09).
5. **"Whenever I feel like it" is not an entry criterion.** No IV-rank filter, no event-calendar
   check (earnings can gap the stock straight through both strikes), no sizing rule.
