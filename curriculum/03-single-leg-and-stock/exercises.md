# 03 — Single Legs & Stock: Exercises

Reason first, then verify calculable parts with `strategies.*` + `analyzer.summarize` in the
notebook. DEMO: spot **$100**, IV **0.25**, **45 DTE**. Chain mids from module 00.

---

### 1. Long call breakeven and max loss (calculation)
You buy the DEMO 100 call for 3.91. (a) What is the expiry breakeven? (b) Max loss in dollars for
one contract? (c) At expiry with the stock at 106, what is your P&L? Verify with
`analyzer.summarize` and `payoff.pnl_at_expiry`.

### 2. Covered call, fully decomposed (calculation)
Long 100 DEMO shares at 100, short the 105 call for 1.85. (a) Max profit (dollars) and the spot at
which it is reached? (b) Downside breakeven? (c) At expiry with the stock at 103, what is your total
P&L (stock + short call)?

### 3. Cash-secured put mindset (scenario judgment)
You sell the DEMO 95 put for 1.58, cash-secured. (a) What is your effective cost basis if assigned?
(b) The stock is at 92 at expiration — are you assigned, and what is your P&L/position? (c) State
the one-sentence mindset that makes this a sound trade rather than "picking up pennies."

### 4. Match the IV regime (scenario judgment)
For each, name a *better* single-leg/stock structure and say why in terms of vega sign:
(a) You are bullish on DEMO; IV Rank is 15. (b) You are bullish on DEMO; IV Rank is 70.
(c) You own 100 shares, are nervous into an event, and IV Rank is 20.

### 5. Covered call vs stock crossover (calculation)
Using the covered call from #2 and plain long stock at 100: (a) Below the short strike, by how much
does the covered call outperform stock at any given price? (b) Above 105, describe how the two
diverge. (c) In what kind of market (name it) does the covered call win?

### 6. Collar economics (calculation)
Long 100 shares at 100, buy the 95 put (1.58), sell the 105 call (1.85). (a) Net debit or credit?
(b) Max loss and max profit in dollars. (c) Why does the skew (module 02) make a *credit* collar
easier to achieve here?

### 7. Protective put drag (scenario)
You hold 100 DEMO shares and buy the 95 put (1.58) every 45 days as standing insurance, four cycles
in a row, while the stock chops sideways around 100. (a) Roughly what have you spent on premium over
the four cycles (ignore any put value at each roll)? (b) What structure would have cut that cost,
and what do you give up to get it?

### 8. Break it (find the flaw)
A trader says: "Cash-secured puts are free money. I'll sell the 45-DTE cash-secured put on the most
volatile small-cap I can find — HIGHVOL-type names, IV 55% — because the premium is huge. I'll do it
on ten different names at once for max income." Identify at least three flaws.

---
---

## Answer key

### 1.
(a) Breakeven = strike + premium = 100 + 3.91 = **103.91**. (b) Max loss = premium × 100 =
**−$391** (stock below 100 at expiry → call worthless). (c) At 106: intrinsic = 6.00, P&L =
(6.00 − 3.91) × 100 = **+$209**. `summarize` shows `max_loss = -391`, breakeven ≈ 103.91;
`pnl_at_expiry(lc, 106)` ≈ 209.

### 2.
(a) Max profit = (105 − 100) + 1.85 = 6.85 → **$685**, reached at any spot **≥ 105** at expiry (you
sell shares at 105, keep the credit). (b) Downside breakeven = stock cost − credit = 100 − 1.85 =
**98.15**. (c) At 103: stock P&L = (103 − 100) × 100 = +300; short 105 call expires worthless →
keep +185. Total = **+$485**.

### 3.
(a) Effective cost basis = strike − premium = 95 − 1.58 = **93.42**. (b) At 92 (below 95) you are
**assigned**: you buy 100 shares at 95, now worth 92. P&L = (92 − 93.42) × 100 = **−$142** (you own
100 shares at a 93.42 basis, i.e. a small paper loss, cushioned by the credit). (c) Mindset: *"I am
getting paid to place a limit buy order at a price I'd happily own the stock."* It is sound only on
a name you genuinely want at that strike — otherwise you are catching a falling knife for pennies.

### 4.
(a) IV Rank 15 (cheap): **long call** (or debit call spread) — you want **long vega/long delta**;
overpaying for vega is not a risk when vol is cheap. (b) IV Rank 70 (rich): **cash-secured put** —
**short vega/positive delta**; collect fat premium and profit as IV mean-reverts. Same bullish
view, opposite structure by IV. (c) IV Rank 20, nervous, own shares: **protective put** — insurance
is *cheaper* when IV is low, and you want the long-vega put that gains if a selloff spikes IV.

### 5.
(a) Below 105 the covered call outperforms plain stock by exactly the **premium collected, 1.85
($185)** at every price (the short call is worthless there, so you simply have stock + credit).
(b) Above 105, plain stock keeps rising point-for-point while the covered call **flatlines at its
+685 cap** — stock wins, and the gap widens the higher it goes. (c) The covered call wins in
**flat, choppy, or mildly bullish** markets — where stocks spend most of their time.

### 6.
(a) Put costs 1.58, call collects 1.85 → net **credit of 0.27 ($27)**. (b) Max loss =
(100 − 95) − 0.27 = 4.73 → **−$473**; max profit = (105 − 100) + 0.27 = 5.27 → **+$527**. (c) The
put skew (module 02) means the 95 put carries higher IV than a symmetric call — but the *call
strike* (105) is where you're happy to sell, and its premium (1.85) still exceeds the put's (1.58),
netting a credit. Skew raises the whole put wing, but choosing a call strike you'd sell at makes the
financing work.

### 7.
(a) ~1.58 × 4 = **~$6.32 per share ≈ $632** in premium over four cycles (before any residual put
value) — a meaningful drag on a stock going nowhere. (b) A **collar** cuts the cost: selling a call
against the position finances the put (here to a net credit). What you give up is **upside above the
call strike** — you cap gains in exchange for cheap/free protection.

### 8.
At least three flaws:
1. **"Free money" ignores max loss.** Each CSP's max loss is (strike − premium) × 100 — large. On
   a 55%-IV small-cap, a gap-down of 20–40% is routine; assignment there is a real, sizeable loss,
   not pennies.
2. **Huge premium is compensation for huge risk, not edge.** High IV means the market expects big
   moves; you are being paid *fairly* for real danger. Selling vol is only smart when it is *rich
   relative to that name's own history* (IV Rank), not just high in absolute terms (module 02).
3. **Ten names at once = concentrated, correlated short-put risk.** In a market-wide selloff, all
   ten gap down together — this is not diversification, it is one big leveraged long-the-market bet
   that pays off slowly and loses fast. Position sizing and correlation (module 10) are ignored.
4. **Selling puts on stocks you would *not* want to own.** The CSP is sound only when assignment is
   acceptable; "most volatile small-cap I can find" is usually the opposite of a name you want to
   hold through a crash.
