# 01 — The Greeks: Exercises

Do these by hand/reasoning first, then verify the calculable ones with `greeks.bsm_greeks` and
`greeks.position_greeks` in the notebook. DEMO: spot **$100**, IV **0.25**, work at **45 DTE**
(`t = 45/365`) unless told otherwise.

---

### 1. Read a delta three ways (scenario)
The DEMO 45-DTE 110 call has delta ≈ 0.20. State what that single number tells you about:
(a) directional exposure per contract, (b) the hedge (how many shares to neutralize one contract),
(c) the rough probability the call expires ITM.

### 2. Share-equivalence and sizing (calculation)
You are long 8 contracts of the DEMO 100 call (delta ≈ 0.53). (a) What is your position delta in
dollar terms? (b) If the stock gaps from 100 to 103 overnight, estimate your P&L from delta alone.
(c) Why is that estimate too *low* rather than too high for an up-move — which greek explains the
difference?

### 3. Gamma sign and pain (scenario judgment)
Trader A is long the 100 straddle; Trader B is short the 100 straddle. Both are roughly
delta-neutral at entry. The stock makes a fast 6% move. (a) Who benefits and who suffers, and
which greek governs it? (b) Why does this asymmetry get *worse* as expiration approaches?

### 4. Theta vs. gamma trade-off (scenario)
You want positive theta (daily income). Your friend says "just also stay long gamma so a big move
helps you too." Explain why you cannot have both on the same option, and what you are really
choosing between.

### 5. Right on direction, wrong on the trade (scenario judgment)
You buy the DEMO 100 call at IV 0.25 for ~3.91. Over the next week the stock rises to 102 **and**
IV falls to 0.20. Using the signs of delta and vega, explain qualitatively why your gain might be
much smaller than "the stock went up $2, I have 0.53 delta, so I made ~$1." Which greek ate your
profit?

### 6. Build position greeks (calculation)
Construct the DEMO bull call spread: long 100 call, short 110 call, 45 DTE. Using per-share deltas
of +0.53 (long) and +0.20 (short): (a) what is the net position delta in dollars for one spread?
(b) Is the spread net long or short vega, and why? (c) Verify with `greeks.position_greeks` in the
notebook.

### 7. Vega and time (calculation)
Compare vega of the ATM 100 call at 7 DTE versus 180 DTE. Which is larger, and by roughly how much
(order of magnitude)? Verify with `bsm_greeks`. What does this imply about *where on the calendar*
you take vega bets?

### 8. Break it (find the flaw)
A trader wants steady income, so she sells the DEMO 100 straddle at **5 DTE** because "the theta is
huge that close to expiration — I collect decay fast." Identify the flaw in leaning into 5-DTE
short premium for income, naming the specific greek that makes this dangerous and what a small
overnight gap would do.

---
---

## Answer key

### 1.
(a) Per contract, delta 0.20 ≈ **20 share-equivalents**: you make/lose ~$20 per $1 move in the
stock. (b) To neutralize one contract you **short 20 shares** (20 deltas of opposite sign).
(c) The call has roughly a **20% chance** of expiring ITM (delta as a risk-neutral probability
proxy — approximate, ignores skew).

### 2.
(a) 8 contracts × 0.53 × 100 = **+424 dollar-deltas** (long, behaves like +424 shares). (b) Delta
estimate: +424 × 3 = **~+$1,272**. (c) It is too low because **gamma is positive** for long
calls: as the stock rises, delta *increases*, so the actual gain accelerates above the straight
delta line. Delta alone is a first-order (linear) estimate; gamma is the curvature that helps a
long-option holder on the way up.

### 3.
(a) **Trader A (long straddle) benefits; Trader B (short straddle) suffers.** The long straddle is
**long gamma** — a fast, large move grows its favorable delta and it profits regardless of
direction; the short straddle is **short gamma** and loses at an accelerating rate. Gamma governs
it. (b) Gamma is **largest near expiration**, so the short-gamma player's losses from a given move
are far more violent close to expiry — the same 6% gap that is uncomfortable at 45 DTE can be
account-threatening at 3 DTE.

### 4.
Theta and gamma are opposite sides of one coin on any option: **long option = positive gamma but
negative theta; short option = positive theta but negative gamma.** To collect positive theta you
must *sell* optionality, which makes you short gamma (exposed to moves). You are really choosing
between **"get paid to wait but be hurt by a big move" (short premium)** and **"pay to wait but be
helped by a big move" (long premium)**. There is no position that pays you theta *and* rewards you
for a move on the same option.

### 5.
Delta is **positive** (long call), so the $2 up-move helps: ~0.53 × 2 ≈ +$1.06/share of gain.
But vega is **positive** too, and IV fell 5 points (0.25→0.20). With vega ≈ 0.13/point, that is
roughly −0.13 × 5 ≈ **−$0.65/share** of loss — plus a few days of negative theta. Net, your gain
shrinks toward ~$0.40 or less instead of the naive ~$1. **Vega ate your profit** — the classic
"right on direction, hurt by the vol drop" outcome. (Exact numbers depend on re-pricing; the
notebook confirms the direction and rough size.)

### 6.
(a) Net delta per spread = (0.53 − 0.20) × 100 = **+33 dollar-deltas** (moderately long). (b) The
spread is **net short vega**: you are long the 100 call's vega but short the 110 call's vega, and
because you *also* sold an option, the short leg trims your total long-vega exposure — a debit
vertical carries small net vega, much less than the outright long call. (Sign can be slightly long
because the ATM long leg has more vega than the OTM short leg; the key point is the short leg
*reduces* net vega versus the naked call.) (c) `position_greeks` on the built spread confirms a
small positive delta (~+33) and a much-reduced vega relative to the lone long call.

### 7.
The **180-DTE ATM call has far larger vega** than the 7-DTE one — vega grows with time to
expiration, roughly several times larger at 180 vs. 7 days. Implication: **take vega (volatility)
bets in longer-dated options**, where a change in IV moves the price meaningfully; short-dated
options are dominated by gamma/theta, not vega. If you want to be long or short *volatility* as
such, the back months are where the exposure lives.

### 8.
The flaw: chasing 5-DTE theta means accepting **enormous negative gamma**. Yes, theta per day is
large that close to expiration — but gamma is *also* largest there, and the two are inseparable.
A short straddle at 5 DTE is nearly delta-neutral and collecting decay, but a **small overnight
gap** (say the $100 stock opens at $104) blows past the modest credit collected: the short-gamma
delta explodes against you and the loss dwarfs several days of theta income. "Huge theta" is the
bait; **short gamma near expiry** is the hook. Income selling is generally done with *more* time
(e.g., 30–45 DTE) and defined risk, and managed *off* before the gamma gets ugly — not leaned into
at 5 DTE naked.
