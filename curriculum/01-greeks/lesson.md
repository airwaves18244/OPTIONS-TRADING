# 01 — The Greeks: The Dials on the Machine

In module 00 you learned that a premium is a small machine with five dials — spot, time, vol,
rates, dividends — and that everything interesting lives in the *extrinsic* part of the price.
The **greeks** are the numbers that tell you how hard each dial pushes the premium. Delta,
gamma, theta, vega, rho. After this module you will be able to look at any option or multi-leg
position and say, without running anything: *if the stock moves a dollar I make or lose about
this much; if a day passes I lose about that much; if implied vol drops two points I gain or
lose this.* That is the difference between hoping a trade works and knowing what it is exposed to.

We keep anchoring to **DEMO**: spot **$100**, IV **~25%**, and we mostly work the **45-DTE**
expiration (`t = 45/365 ≈ 0.1233`).

---

## 1. What a greek is

A greek is a **sensitivity** — the partial derivative of the option's price with respect to one
input, holding the others fixed. You do not need calculus to use them; you need to read them as
*rates of change per unit*, and you must know the units, because this library's conventions are
specific (from `SPEC.md`):

- **delta** — price change **per $1** move in spot, **per share**.
- **gamma** — change in *delta* per $1 move in spot.
- **theta** — price change **per calendar day** (annual theta ÷ 365). Usually negative for long
  options.
- **vega** — price change per **1 vol point**, i.e. IV up by 0.01 (one percentage point).
- **rho** — price change per **+1%** (0.01) move in the interest rate.

For a **single option**, greeks are quoted **per share**. For a **position**, `optionslab`
aggregates them into **dollars** — multiplying by `quantity × multiplier` and summing across legs.
That dollar aggregation is what makes position greeks directly actionable: a position delta of
+250 means "this position behaves like being long 250 shares — up $250 per $1 the stock rises."

---

## 2. Delta — direction, share-equivalence, and a probability proxy

**Delta is the workhorse.** It answers: *if the stock moves up $1, how much does the option price
move?*

- **Long call delta** runs from **0 to +1**. Deep OTM ≈ 0 (the option barely reacts); ATM ≈ 0.5;
  deep ITM ≈ +1 (the option moves dollar-for-dollar with the stock, like owning shares).
- **Long put delta** runs from **0 to −1**. Deep OTM ≈ 0; ATM ≈ −0.5; deep ITM ≈ −1.
- **Short** options flip the sign: a short call has *negative* delta, a short put *positive*.

On DEMO at 45 DTE, the ATM 100 call has delta ≈ **0.53** (slightly above 0.5 because of drift and
the lognormal shape). The 110 call, well OTM, has delta ≈ **0.20**. The 90 call, ITM, ≈ **0.83**.

### Three ways to read delta

1. **Directional exposure.** Delta is your *share-equivalent* position. A 0.53-delta call is like
   owning 53 shares (per contract, since 0.53 × 100). If you are long 5 of those calls, you have
   +265 deltas — you make ~$265 per $1 up-move, lose ~$265 per $1 down. This is how you size
   directional risk.
2. **Hedge ratio.** To neutralize the directional risk of one 0.53-delta call, you would short 53
   shares. This is *delta hedging*, and it is the basis of "delta-neutral" trading (section 7).
3. **Rough probability of finishing ITM.** An option's delta approximates the risk-neutral
   probability it expires in-the-money. A 0.20-delta call has *roughly* a 20% chance of finishing
   above its strike; a 0.16-delta short strike (a number you will meet constantly in module 05)
   sits near the 1-standard-deviation move — about an 84% chance of expiring OTM, i.e. worthless,
   which is exactly why premium sellers love it. Treat this as a *proxy*, not gospel: it ignores
   skew and is a risk-neutral, not real-world, probability. But as a quick read it is invaluable.

**Delta is not constant.** As the stock moves, delta changes — and the speed of that change is
the next greek.

---

## 3. Gamma — the speed of delta, and why it explodes near expiry

**Gamma** measures how fast delta changes as the stock moves. High gamma means your delta — your
directional exposure — shifts quickly under your feet.

- Gamma is **highest for ATM options** and **highest close to expiration**. An ATM option a week
  from expiry has ferocious gamma; the same strike 90 days out has gentle gamma.
- **Long options (calls or puts) have positive gamma**; **short options have negative gamma.**
  This sign is the heart of a lot of pain and profit.

Why does it matter? Positive gamma is *helpful*: as the stock moves in your favor, your delta
grows in your favor (you make money at an accelerating rate); as it moves against you, your delta
shrinks (you lose at a decelerating rate). The long-option holder's curve bends the friendly way.

**Negative gamma is the seller's curse.** If you are short options, an adverse move makes your
losing delta *grow* — you lose faster and faster the more wrong you get. This is why short-premium
strategies (modules 04–05) feel fine until they suddenly do not, especially in the last week when
gamma is largest. The phrase to remember: **short premium is short gamma; near expiry, short
gamma bites.** On DEMO, a short ATM straddle at 7 DTE has trivial theta income compared to the
gamma risk of a 3% overnight gap. Managing that trade-off — collecting theta without getting run
over by gamma — is a recurring theme from module 05 onward.

---

## 4. Theta — the rent on time

**Theta** is the price change per calendar day, from nothing but the clock advancing. For long
options it is **negative** (you lose value daily); for short options it is **positive** (you
collect).

- Theta is **largest (most negative for longs) for ATM options** and **accelerates into
  expiration** — the mirror image of the extrinsic-value decay you saw in module 00.
- Theta and gamma are **opposite sides of one coin.** The option seller earns theta but carries
  negative gamma; the buyer pays theta but owns positive gamma. There is no free lunch: *you
  cannot be long gamma and long theta at the same time on the same option.* If someone is paying
  you to wait (positive theta), you are exposed to the move (negative gamma), and vice versa.

On DEMO, the 45-DTE ATM 100 call carries theta ≈ **−0.03** per day (about $3 per contract per
day). That does not sound like much until you remember it accelerates: the same strike at 7 DTE
might bleed $8–10 per contract per day. Sellers position to *harvest* that steepening curve;
buyers must overcome it with a move.

---

## 5. Vega — exposure to the market's fear

**Vega** is the price change per one-point (0.01) rise in implied volatility. It is the dial
beginners never look at and the one that quietly decides many trades.

- **Long options have positive vega** (rising IV inflates their extrinsic value); **short options
  have negative vega.**
- Vega is **largest for ATM options** and **grows with time to expiration** — long-dated options
  are far more vega-sensitive than weeklies. A 180-DTE ATM DEMO option has several times the vega
  of a 7-DTE one.

On DEMO at 45 DTE, the ATM 100 call has vega ≈ **0.13** — meaning if IV rises from 25% to 26%,
the option gains about $0.13/share ($13/contract), all else equal. Now the crucial consequence,
foreshadowing module 02: **you can be right on direction and lose money because vega moved against
you.** Buy a call before earnings, the stock rises as you predicted, but IV collapses from 55% to
30% afterward (the "vol crush") — your positive delta gain is swamped by your positive-vega loss.
Understanding vega is what separates traders who *trade volatility on purpose* from those who get
blindsided by it.

**"Short vega"** means the position *profits when IV falls* and loses when IV rises. Selling
premium (credit spreads, iron condors, short strangles) is inherently short vega — you want the
market's fear to subside after you sell it. That is why these are **high-IV strategies**: you sell
when vega exposure is richly paid and profit as it mean-reverts down.

---

## 6. Rho — the dial you can mostly ignore (until you can't)

**Rho** is the price change per 1% move in interest rates. For the short-dated retail trades that
dominate this curriculum, rho is a minor character — a 45-DTE ATM option's rho is a few cents.
It matters for **long-dated options** (LEAPS, the poor man's covered call in module 06) and in
**high-rate environments**, where the cost of carry meaningfully affects call and put values and
feeds into early-assignment decisions on short puts. Know it exists, know it scales with time to
expiration and with rates, and move on. We will not belabor it.

---

## 7. Position greeks: adding the dials across legs

Real trades have multiple legs, and greeks **add**. The `Greeks` dataclass in this library is
*addable and scalable* precisely so you can sum them. `position_greeks(pos, spot, vol)` does the
aggregation for you: each option leg contributes `bsm_greeks(...) × quantity × multiplier`, stock
legs contribute `delta = quantity` (and zero for the rest), and remaining time is honored per leg.
The result is in **dollars per unit** — directly the P&L sensitivity of the whole position.

Two worked intuitions on DEMO (spot 100, 45 DTE):

**A bull call spread** — long the 100 call (delta ≈ +0.53), short the 110 call (delta ≈ +0.20).
Net delta ≈ +0.33 per share, or **+33 dollar-deltas** per one-lot spread. You are moderately long
direction. The short leg also *cuts your vega and your theta*: by selling the 110 call you give
back some negative-theta pain and some positive-vega exposure. That is the whole point of a
spread — it trims the greeks you do not want to pay for.

**A short straddle** — short the 100 call and short the 100 put. The deltas roughly cancel
(−0.53 + +0.47 ≈ **−0.06**, near zero), so the position starts **delta-neutral**. But both legs
are short, so it is **short gamma** (dangerous on big moves), **positive theta** (you collect
decay every day), and **short vega** (you profit if IV falls). This is the canonical
*delta-neutral, short-vega, positive-theta* structure.

### What "delta-neutral, short-vega" means as a book

When a trader says their book is **delta-neutral and short-vega**, they mean: net share-equivalent
exposure ≈ 0 (no directional bet — small moves either way barely matter), and net vega < 0 (they
profit if implied volatility falls). Such a book earns **theta** (time decay) as its edge and is
exposed to **gamma** (a big fast move hurts, because short gamma) and to a **vol spike** (vega
loss). That single sentence — *neutral on direction, short on vol, long on time, short on gamma* —
describes the risk profile of most premium-selling income strategies you will build in module 05.
Position greeks are how you *verify* a book actually is what you intend it to be, rather than
carrying a hidden directional or vol bet you did not mean to take.

---

## 8. P&L attribution: reading a day through the greeks

The greeks are not just a pre-trade profile; they are a **language for explaining what happened**.
At the end of any trading day you can decompose your position's P&L into the pieces each greek
contributed — this is *P&L attribution*, and doing it (even roughly, in your head) is how you learn
to see which risk actually paid or hurt you.

The first-order approximation is a Taylor expansion of the position value:

```
ΔP&L ≈ delta × Δspot + ½ × gamma × (Δspot)² + theta × Δdays + vega × ΔIV
```

Work a concrete DEMO example. You are long one 100 call (per-share greeks: delta ≈ 0.53, gamma ≈
0.045, theta ≈ −0.03, vega ≈ 0.13). Overnight the stock rises **+2.00**, one day passes, and IV
*falls* one point (−0.01). Per share:

- **delta** contributes 0.53 × 2.00 = **+1.06** — the bulk of the gain, from direction.
- **gamma** contributes ½ × 0.045 × 2.00² = **+0.09** — the bonus from delta growing as you went
  ITM (positive gamma helping a long).
- **theta** contributes −0.03 × 1 = **−0.03** — one day's rent.
- **vega** contributes 0.13 × (−1) = **−0.13** — the vol dip nicked you (you're long vega).

Sum ≈ **+0.99/share**, or ~+$99 on the contract. Notice the story the numbers tell: you made money
*because you were right on direction*, gamma sweetened it, and a small vol slip plus a day of decay
shaved a little off. Had IV instead *dropped five points* (−0.05), the vega term becomes −0.65 and
your gain shrinks to ~+$0.34 — the "right on direction, hurt by vol" outcome, quantified. This is
exactly the decomposition the module-02 vol-crush warning is about, and it is why professionals
never say "I made money because the stock went up" without checking whether vega and theta were
tailwinds or headwinds. The notebook lets you re-price the position exactly and compare the true
P&L to this greek-based estimate — they agree closely for small moves and diverge for large ones
(where higher-order terms matter, which is precisely what gamma is warning you about).

## 9. How the greeks move with moneyness, time, and vol — a summary map

Commit this table to memory; it is the mental model the rest of the curriculum assumes.

| Greek | Sign (long) | Biggest when… | Grows / shrinks as expiry nears |
|-------|-------------|---------------|----------------------------------|
| delta | call +, put − | deep ITM (→±1) | ITM→±1, OTM→0 (sharpens) |
| gamma | + | **ATM** | **grows** (explodes ATM near expiry) |
| theta | − | **ATM** | **grows** (decay accelerates) |
| vega  | + | **ATM** | **shrinks** (short-dated = low vega) |
| rho   | call +, put − | deep ITM, long-dated | shrinks |

Read the three "biggest when ATM" rows together: **gamma, theta, and vega all peak at the money.**
That is why ATM options are the most *alive* — the most reactive to time and vol — and why so many
strategies pivot around ATM and near-ATM strikes. Read the "as expiry nears" column together and
you see the seller's dilemma in one glance: as expiration approaches, the theta you want to
collect grows, but so does the gamma that can hurt you — while the vega exposure fades.

---

## Key takeaways

- Greeks are **per-unit sensitivities**: delta per $1 spot, gamma the speed of delta, theta per
  calendar day, vega per 1 vol point, rho per 1% rate. Single options: per share; **positions:
  dollar-aggregated** via `quantity × multiplier`.
- **Delta** is directional exposure *and* your share-equivalent hedge ratio *and* a rough
  ITM-probability proxy (a ~16-delta option ≈ 1σ OTM). It is not constant.
- **Gamma** is delta's speed — highest ATM and near expiry. **Long = positive gamma** (moves help
  you); **short = negative gamma** (the seller's curse, worst near expiry).
- **Theta** is time decay: negative for buyers, positive for sellers, accelerating into
  expiration. Gamma and theta trade off — you cannot be long both.
- **Vega** is IV exposure: long options are long vega, short options short vega; largest ATM and
  for long-dated options. **You can be right on direction and lose on vega** — the vol crush.
- **Position greeks add across legs.** "Delta-neutral, short-vega" = no directional bet, profits
  when IV falls, earns theta, exposed to gamma and vol spikes — the signature of income strategies.

## In the next module

Vega tells you *how much* an option reacts to implied volatility. **Module 02** is about IV
itself: historical vs. implied vol, IV rank and percentile, skew, term structure, and event vol —
the single most important input to *which* strategy you should even be running.
