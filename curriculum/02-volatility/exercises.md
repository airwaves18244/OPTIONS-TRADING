# 02 — Volatility: Exercises

Reason first, then verify the calculable parts in the notebook with `pricing.implied_vol`,
`analyzer.expected_move`, and the sample chains. DEMO spot **$100**.

---

### 1. HV from returns (calculation)
A stock's daily log returns over a stretch have a sample standard deviation of 0.014 (1.4%).
Estimate the annualized historical volatility. (Use √252 ≈ 15.87.) Is that stock more or less
volatile than DEMO (IV ~25%)?

### 2. Back out the IV (calculation)
The DEMO 45-DTE 100 call trades at a mid of 3.91. Using `pricing.implied_vol`, what IV reproduces
that price (rate and dividend 0)? Then price a call with that IV via `bsm_price` and confirm you
get 3.91 back. What property is this demonstrating?

### 3. Rich or cheap? (scenario judgment)
Over the past year, stock XYZ's IV ranged from a low of 20% to a high of 60%; today it is 32%.
(a) Compute its IV Rank. (b) Is IV rich or cheap in XYZ's own terms? (c) Does this bias you toward
buying or selling premium, and why (name the vega sign)?

### 4. Read the skew (calculation/interpretation)
From the DEMO 45-DTE chain, compare the IV of the 85 put, the 100 (ATM) options, and the 115 call.
Which is highest? Name the pattern and give the two structural reasons OTM puts trade rich. What
does this imply about which *side* of a premium-selling trade pays more?

### 5. Term structure shape (scenario judgment)
DEMO's ATM IV runs about 0.269 at 7 DTE and 0.253 at 180 DTE. (a) Is that contango or
backwardation? (b) What does the shape hint about near-term risk? (c) Which module-06 structure is
a direct trade on this shape, and which leg (front or back) would you sell?

### 6. Implied move and the crush (scenario judgment)
A $100 stock reports earnings tomorrow. Its event-week ATM straddle costs about 7.00. (a) What
one-standard-deviation move is the market implying (roughly)? (b) You buy that straddle; the stock
gaps to 105 and IV collapses from 60% to 30%. Are you guaranteed a profit? Explain using delta and
vega. (c) Reframe what you were *really* betting on when you bought the straddle.

### 7. Same view, two structures (scenario judgment)
You are **moderately bullish** on DEMO over the next 45 days. Give the smart structure if
(a) DEMO's IV Rank is 12, and (b) DEMO's IV Rank is 68. Justify each choice by the sign of vega you
want given the IV regime.

### 8. Break it (find the flaw)
A trader brags: "I only sell options when IV is above 25% — that's high, so I'm always selling
expensive premium." Identify the conceptual error in using an absolute IV threshold across
different underlyings, using LOWVOL (IV ~14%) and HIGHVOL (IV ~55%) as counterexamples.

---
---

## Answer key

### 1.
Annualized HV = 0.014 × √252 ≈ 0.014 × 15.87 ≈ **0.222 = 22.2%**. That is **slightly less
volatile** than DEMO's ~25% IV. (Note this compares realized HV to implied IV — if this 22% HV
were DEMO's own realized vol, it would hint DEMO's 25% IV is pricing in a bit *more* movement than
the stock has recently delivered, a mild lean toward selling.)

### 2.
`pricing.implied_vol('call', price=3.91, spot=100, strike=100, t=45/365)` returns approximately
**0.262** (26.2%). Feeding that back: `bsm_price('call', 100, 100, 45/365, 0.262)` ≈ **3.91**.
This demonstrates the **round-trip property**: `implied_vol` and `bsm_price` are inverses —
IV is defined as exactly the vol that reproduces the market price.

### 3.
(a) IV Rank = (32 − 20) / (60 − 20) × 100 = 12/40 × 100 = **30**. (b) At the **low end** of its
range — IV is **cheap** in XYZ's own terms. (c) Bias toward **buying** premium (debit strategies,
**long vega**): you want to own cheap volatility and profit if IV mean-reverts *up* (or if realized
movement exceeds the low implied level). Selling here would collect too little for the vega risk.

### 4.
The **85 put has the highest IV** (~0.296), the ATM ~0.262, and the 115 call the lowest (~0.248).
The pattern is **put skew** (a downward smirk). OTM puts trade rich because (1) **crash-risk
asymmetry** — stocks fall faster/more violently than they rise, so more tail risk is priced into
downside strikes; and (2) **structural protection demand** — funds persistently buy OTM puts as
insurance, often financed by selling OTM calls. Implication: the **put side** of a premium-selling
trade (cash-secured puts, put credit spreads, the put wing of a condor) collects *more* premium —
you are paid extra for taking the side the market fears.

### 5.
(a) Front IV (0.269) > back IV (0.253): **backwardation** (downward-sloping). (b) It hints at
elevated **near-term** risk the market expects to resolve — some event or nervousness front-loaded
into the near expirations. (c) A **calendar spread** (module 06) trades this shape directly; you
**sell the front-month** (richer vol) and **buy the back-month** (cheaper vol), wanting the term
structure to normalize/flatten.

### 6.
(a) One-sigma implied move ≈ the ATM straddle price ≈ **7 points (~7%)**, so the market prices
roughly a move to 93 or 107. (More precisely, `expected_move = spot × IV × √t`; the straddle is a
close proxy.) (b) **Not guaranteed.** You are long delta on the call side but the stock only moved
+5 (less than the ~7 implied), and you are **long vega** into a **20-point IV crush** (60%→30%),
which deflates both legs hard. The vega loss can exceed the intrinsic gain from the 5-point move —
you can lose while being directionally "right." (c) You were really betting that **realized
movement would exceed the implied move (~7)** — a bet on *magnitude vs. what was priced*, not on
direction. The stock's 5-point move came in *under* the implied move, so the short-vol side won.

### 7.
(a) IV Rank 12 (cheap): buy premium — a **long call** or a **debit (bull) call spread**. You want
**long vega / long delta** because volatility is cheap; overpaying for vega is not a risk here.
(b) IV Rank 68 (rich): sell premium — a **cash-secured put** or a **bull put (credit) spread**.
You want **short vega / positive delta**, collecting richly priced premium and profiting as IV
mean-reverts down. Same bullish view, opposite vega sign, chosen by the IV regime.

### 8.
The error is using an **absolute** IV threshold across underlyings whose *normal* IV levels differ
wildly. 25% is **high** for **LOWVOL** (which normally lives near 14% — so at 25% you would indeed
be selling rich vol) but **very low** for **HIGHVOL** (which normally sits near 55% — selling 25%
premium there means selling *cheap* vol, undercompensated for the real movement that stock
delivers). "High IV" is only meaningful **relative to each name's own history** (IV Rank /
Percentile). A flat 25% rule sells cheap vol on volatile names and might skip genuinely rich
setups on calm ones.
