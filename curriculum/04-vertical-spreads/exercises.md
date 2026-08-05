# 04 — Vertical Spreads: Exercises

Reason first, then verify with `strategies.*` + `analyzer.summarize`. DEMO: spot **$100**, IV
**0.25**, **45 DTE**. Chain mids from module 00.

---

### 1. Bull call spread, fully specified (calculation)
Buy the 100 call (3.91), sell the 110 call (0.73). (a) Net debit? (b) Max loss, max profit, and
breakeven? (c) Confirm max profit + max loss equals the width × 100.

### 2. Credit spread arithmetic (calculation)
Sell the 95 put (1.58), buy the 90 put (0.62) — a bull put spread. (a) Net credit? (b) Max profit,
max loss, breakeven? (c) At expiry with DEMO at 93, what is your P&L?

### 3. Same view, pick the expression (scenario judgment)
You are moderately bullish on DEMO over 45 days. Choose bull *call* spread vs bull *put* spread if:
(a) DEMO's IV Rank is 18; (b) DEMO's IV Rank is 65. Justify each by vega sign and by what has to
happen for the trade to win.

### 4. The 50% rule (scenario)
You sold the bull put spread in #2 for a 0.96 credit. Two weeks later, with DEMO flat, it's worth
0.46 to buy back. (a) What is your open P&L in dollars? (b) The "take it at 50%" rule says to do
what, and why give up the remaining theoretical profit? (c) What annualized-efficiency argument
supports closing early?

### 5. POP vs max profit (calculation/interpretation)
Compare two bull put spreads, both 5 wide: short 97.5 / long 92.5 vs short 90 / long 85. Using the
notebook, state which has higher POP and which has higher credit/max profit. Explain why you cannot
get both, in one sentence.

### 6. Width and sizing (scenario)
A bull put spread with a 5-wide width and 0.96 credit risks $404. You want to risk no more than
$1,000 on the idea. (a) How many spreads can you sell? (b) If you instead used a 10-wide version
risking ~$800 per spread, how many, and what changes about your max profit and capital at risk?

### 7. Skew and the bear call (scenario judgment)
You want a neutral-to-bearish credit trade. You notice the call-side credits are thinner than the
equivalent put-side credits at the same delta. (a) Why (module 02)? (b) Does that make the bear
call spread a bad trade, or just differently priced? (c) What early-assignment risk is unique to
the short *call* leg?

### 8. Break it (find the flaw)
A trader's plan: "I sell the 45-DTE bull put spread as close to the money as possible — short the
100 put — for the biggest credit, and I always hold to expiration to collect every penny of max
profit. High credit, and I keep it all." Identify at least three flaws.

---
---

## Answer key

### 1.
(a) Net debit = 3.91 − 0.73 = 3.18 → **$318**. (b) Max loss = debit = **−$318** (DEMO ≤ 100);
max profit = width − debit = 10 − 3.18 = 6.82 → **+$682** (DEMO ≥ 110); breakeven = 100 + 3.18 =
**103.18**. (c) 682 + 318 = **$1,000** = width (10) × 100. ✓

### 2.
(a) Net credit = 1.58 − 0.62 = 0.96 → **$96**. (b) Max profit = credit = **+$96** (DEMO ≥ 95);
max loss = width − credit = 5 − 0.96 = 4.04 → **−$404** (DEMO ≤ 90); breakeven = 95 − 0.96 =
**94.04**. (c) At 93: the 95 put is 2.00 ITM, the 90 put worthless. Spread value = −2.00; P&L =
credit − value = 0.96 − 2.00 = −1.04/share → **−$104** (between breakeven 94.04 and max loss).

### 3.
(a) IV Rank 18 (cheap): **bull call spread** (debit). It's **long vega**, so you're not overpaying
when vol is low, and it benefits if IV rises. To win, DEMO must *rise* above the 103.18 breakeven.
(b) IV Rank 65 (rich): **bull put spread** (credit). It's **short vega**, collecting fat premium and
profiting as IV mean-reverts down. To win, DEMO must merely *stay above 95* — it can rise, sit, or
drift down a little. Same bullish view, opposite vega, chosen by IV.

### 4.
(a) Sold for 0.96, now 0.46 → open profit 0.50/share = **+$50** (about 52% of the $96 max). (b) The
rule says **close it now for ~50% of max profit**. You give up the remaining ~$46 because the last
half of the profit takes *disproportionately longer* and exposes you to gamma/tail risk near
expiration for shrinking reward. (c) Closing early frees the capital (the $404 of risk) to redeploy;
capturing 50% of the credit in a third of the time is a far higher *annualized* return than
grinding out the last pennies — and it raises win consistency.

### 5.
The **short-90/long-85** spread has the **higher POP** (short strike further OTM, ~16-delta), while
the **short-97.5/long-92.5** spread has the **higher credit / max profit** (short strike closer to
the money, ~40-delta). You cannot get both because **the market prices probability against payoff**
— a strike that's more likely to expire worthless is worth less premium to sell.

### 6.
(a) $1,000 / $404 ≈ 2.47 → **2 spreads** (max loss ~$808; never round up past your risk cap).
(b) A 10-wide spread risking ~$800 → **1 spread** fits the $1,000 cap. The single 10-wide has a
larger absolute max profit than one 5-wide but you hold fewer units; capital at risk is similar
(~$800 vs ~$808). The choice is granularity vs. a bigger single position — 5-wides let you scale
and manage in smaller increments.

### 7.
(a) **Put skew** (module 02): OTM puts carry higher IV than equidistant OTM calls, so at the same
delta the put fetches more premium — the call wing sits on cheaper vol. (b) Not a bad trade — just
**differently priced**; the thinner credit reflects lower option richness on that side. You simply
adjust expectations (or width) accordingly. (c) The short **call** can be **assigned early** if DEMO
pays a dividend and the call goes deep ITM near the ex-dividend date, when its remaining extrinsic
value drops below the dividend (module 00) — a risk the short *put* side doesn't share for
dividends.

### 8.
At least three flaws:
1. **Selling ATM (short 100 put) maximizes credit but minimizes POP.** A ~50-delta short strike
   loses roughly half the time; the fat credit is compensation for a coin-flip, not free money.
2. **Holding to expiration violates the 50% rule and courts gamma/pin risk.** The last portion of
   profit accrues slowly while the risk of a late adverse move (and assignment/pin at the short
   strike) rises sharply — the opposite of the risk/reward that made the trade attractive.
3. **No loss trigger and no roll plan.** "Keep it all" ignores that a tested short strike can turn
   the $96 credit into a $404 loss fast; a disciplined seller has a ~2× credit stop and a
   roll-for-credit plan (module 09).
4. **IV regime ignored.** "Biggest credit" says nothing about whether IV is *rich* — selling ATM in
   low IV is undercompensated for the real risk taken (module 02).
