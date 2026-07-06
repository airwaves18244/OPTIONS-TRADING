# 00 — Foundations: Exercises

Work these before opening the answer key. Where a problem says "verify in the notebook," do the
arithmetic by hand first, then confirm with `optionslab`. Spot is **$100** on DEMO unless stated.

---

### 1. Dollars, not decimals (calculation)
The DEMO 45-DTE 105 call quotes 1.83 / 1.86. (a) What does one contract cost to buy, in dollars,
if you pay the ask? (b) How much notional stock value does that one contract control? (c) If you
bought ten contracts, what is your total cash outlay and total notional?

### 2. Decompose the premium (calculation)
For each option below (DEMO, 45 DTE, spot 100), split the mid premium into intrinsic and extrinsic
value:
- 90 call, mid 11.07
- 100 call, mid 3.91
- 95 put, mid 1.58
- 110 put, mid 10.19

Which one carries the *most* extrinsic value, and why does that make sense?

### 3. The clock (scenario)
The DEMO ATM 100 call is worth about 3.91 at 45 DTE, 2.66 at 21 DTE, and 1.52 at 7 DTE — with the
stock pinned at 100 the entire time. (a) How much value is lost from 45→21 DTE versus 21→7 DTE?
(b) The second window is shorter in calendar days but the *rate* of loss is higher — explain why
in one sentence. (c) If you are the person who *sold* this call, is this good or bad for you?

### 4. Moneyness that moves (scenario)
You hold the DEMO 105 call. Classify its moneyness (ITM/ATM/OTM) if the stock is at: 100, 105,
112. For each, state the option's intrinsic value.

### 5. Early assignment judgment (scenario judgment)
You are short one DEMO-like 90 call, deep ITM, on a stock now trading at $103. The call's remaining
extrinsic value is $0.05. The stock goes ex-dividend tomorrow, paying $0.60 per share. (a) Should
you expect to be assigned tonight? Show the comparison that decides it. (b) What is the concrete
consequence if you are assigned? (c) What could you have done earlier to avoid it?

### 6. Reading liquidity (scenario judgment)
Two DEMO 45-DTE options:
- 100 call: bid 3.89 / ask 3.93, OI 8,118, volume 2,028
- 130 call: bid 0.00 / ask 0.02, OI 385, volume 19

You want a quick in-and-out trade. Which is tradeable and which is a trap? Quantify the round-trip
spread cost of each as a percentage of the option's mid price.

### 7. Net debit or credit? (calculation)
You simultaneously **buy** the DEMO 100 call (mid 3.91) and **sell** the DEMO 110 call (mid 0.73),
same expiry, one contract each. (a) Is the net a debit or a credit, and how many dollars? (b) What
sign will `Position.net_premium()` report? (c) Verify in the notebook by building the position with
`strategies.bull_call_spread` and calling `net_premium()`.

### 8. Break it (find the flaw)
A new trader says: "I'll buy the DEMO 120 call, 45 DTE, for 0.07 — only $7 a contract. If the
stock even twitches up I double my money, and I can only lose seven bucks. Free lottery ticket, so
I'll buy 300 of them." Identify at least three things wrong or dangerously incomplete in this
reasoning.

---
---

## Answer key

### 1.
(a) Ask is 1.86 per share × 100 = **$186** per contract. (b) Notional = strike × 100 = 105 × 100 =
**$10,500** controlled. (c) Ten contracts: cash outlay 186 × 10 = **$1,860**; notional 10,500 × 10
= **$105,000**. The point: $1,860 of premium is controlling $105,000 of stock — roughly 56:1
leverage. That is why "only $186" is the wrong way to think about size.

### 2.
Intrinsic = `max(S−K,0)` for calls, `max(K−S,0)` for puts; extrinsic = mid − intrinsic.
- 90 call: intrinsic 10.00, extrinsic **1.07**
- 100 call: intrinsic 0.00, extrinsic **3.91**
- 95 put: intrinsic 0.00 (spot 100 > strike 95, so OTM), extrinsic **1.58**
- 110 put: intrinsic 10.00 (strike 110 > spot 100), extrinsic **0.19**

The **100 call carries the most extrinsic value (3.91)** because it is at-the-money: the outcome
is maximally uncertain, so the market charges the most for the possibility of movement. Deep-ITM
and deep-OTM options carry less extrinsic value — the ITM one is dominated by locked-in intrinsic,
the OTM one is a long shot.

### 3.
(a) 45→21 DTE: 3.91 − 2.66 = **$1.25** lost. 21→7 DTE: 2.66 − 1.52 = **$1.14** lost. (b) The
21→7 window is only 14 days versus 24 days, yet loses nearly as much — because time decay
accelerates as expiration approaches (extrinsic value falls with roughly the square root of time
remaining, so the daily bleed steepens near the end). (c) As the **seller**, decay is your
income: you *want* the stock to sit still and the extrinsic value to melt into your pocket. Good
for you.

### 4.
The 105 call:
- Spot 100 → **OTM**, intrinsic **0.00** (105 > 100).
- Spot 105 → **ATM**, intrinsic **0.00** (at the strike).
- Spot 112 → **ITM**, intrinsic **7.00** (112 − 105).

Moneyness is not fixed to the contract; it tracks where spot sits relative to the strike as the
stock moves.

### 5.
(a) The decision compares **dividend captured vs. extrinsic value forfeited by exercising early.**
Dividend = $0.60/share; remaining extrinsic = $0.05/share. Because $0.60 > $0.05, a rational call
holder exercises tonight to capture the dividend, throwing away only $0.05 of time value to gain
$0.60. So **yes, expect assignment.** (b) You are assigned: you must deliver 100 shares at $90.
If you did not already own them, you are now **short 100 shares** at $90 into a stock trading
$103 — an unhedged, capital-intensive position, and you miss/pay the dividend. (c) You could have
**bought the call back (closed the short) or rolled it** before the ex-dividend date, once you saw
it was deep ITM with extrinsic value below the dividend. Watching remaining extrinsic value versus
the upcoming dividend is the whole early-assignment early-warning system.

### 6.
- 100 call: spread = 3.93 − 3.89 = 0.04; mid 3.91; round-trip spread cost ≈ 0.04 / 3.91 ≈
  **1.0%**. OI 8,118, volume 2,028 — **tradeable**.
- 130 call: spread = 0.02 − 0.00 = 0.02; mid 0.01; round-trip cost ≈ 0.02 / 0.01 = **200%** of the
  option's value. Thin OI, almost no volume — **a trap.** You would pay the entire value of the
  option (and more) just crossing the spread. Liquidity first, always.

### 7.
(a) You pay 3.91 for the long call and collect 0.73 for the short call: net = 3.91 − 0.73 = 3.18
per share × 100 = **$318 debit** (cash out). (b) `net_premium()` reports **+318** (positive =
debit). (c) In the notebook, `strategies.bull_call_spread((100, 3.91), (110, 0.73),
expiry=45/365)` then `.net_premium()` should return **318.0**.

### 8.
At least three problems:
1. **Sizing by premium, not by risk/notional.** 300 contracts at $7 is $2,100 — but it is also
   300 × $12,000 = $3.6M of notional. The "only $7" framing hides real exposure and, more to the
   point, it is $2,100 the trader will almost certainly lose in full.
2. **The odds are terrible.** The 120 call is 20% OTM with 45 days to run and prices at 0.07 —
   the market is telling you it is a long shot. Extrinsic-only, deep OTM options usually expire
   worthless; "if it twitches up" ignores that it needs a *large* move to pay.
3. **Time decay works against a buyer every day.** Nothing has to go wrong — the stock sitting
   still guarantees the position bleeds to zero. It is not a "free" ticket; it is rent paid to
   the seller.
4. **Liquidity.** Far-OTM options like this have wide spreads (recall the 130 call at 0.00/0.02);
   getting 300 contracts in and out at a fair price is unrealistic, and the spread alone can be a
   large fraction of the premium.
5. **"Double my money" is not an edge.** A positive-payoff scenario is not the same as positive
   *expected value*. Lottery tickets have huge payoffs and negative expectancy; so does this.
