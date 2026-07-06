# 02 — Volatility: The Option Trader's Raw Material

Here is the mental shift that turns a gambler into a trader. A stock trader has one question:
*which way will it go?* An options trader has two: *which way, and how much will it move relative
to what the market has already priced in?* That second question is **volatility**, and it is the
raw material you are actually buying and selling. Every premium in module 00 had an extrinsic
component; every vega in module 01 measured exposure to one number. This module is about that
number — where it comes from, how to tell if it is high or low, and why **"is IV rich or cheap
right now?"** is the single most important input to *which strategy you should run at all*.

Anchor as always to **DEMO**: spot **$100**, and an IV that sits around **25%**. We will also use
the two other sample chains — **LOWVOL** (spot 185, IV ~14%) and **HIGHVOL** (spot 62, IV ~55%) —
to see what different vol regimes actually look like in a chain.

---

## 1. Two volatilities: historical and implied

**Historical volatility (HV)**, also called realized or statistical volatility, is a *backward*
measurement: how much the stock actually moved over some past window, annualized. You compute it
from the price series — the standard deviation of daily log returns, scaled by √252 (there are
about 252 trading days a year). If DEMO's daily returns had a standard deviation of 1.5%, its
annualized HV would be roughly 0.015 × √252 ≈ **24%**. HV is a fact about the past.

**Implied volatility (IV)** is a *forward* number: the volatility that, plugged into the pricing
model, makes the model spit out the option's *current market price*. It is the market's collective
bet on how much the stock will move *between now and expiration*. You do not choose IV; you back
it out. That is exactly what `pricing.implied_vol` does — give it a market price and it solves for
the vol that reproduces it. When the DEMO 100 call trades at 3.91 with 45 days left, the IV that
reproduces 3.91 is ~0.262 — that is what "implied" means.

**The relationship is the whole game.** IV is the *price* of future movement; HV is the *cost of
what movement actually delivered*. When you **buy** an option you are long IV and you need realized
movement (future HV) to *exceed* the IV you paid, or theta grinds you down. When you **sell** an
option you are short IV and you profit if realized movement comes in *below* the IV you sold. A
useful way to say it: **IV is the market's forecast of future HV, and you are betting the forecast
is wrong** — too high (sell) or too low (buy).

---

## 2. IV is only meaningful *relative to itself*

Beginners ask "is 25% IV high?" The honest answer is *compared to what?* Twenty-five percent is
cripplingly high for a sleepy utility and absurdly low for a biotech before an FDA decision. An
absolute IV number is nearly useless. IV only means something **relative to the underlying's own
history.** Two standard tools make it relative:

**IV Rank (IVR)** — where today's IV sits between its 1-year low and high, as a percentage:

```
IV Rank = (current IV − 52-week low IV) / (52-week high IV − 52-week low IV) × 100
```

If DEMO's IV ranged from 18% to 42% over the past year and today it is 25%, IV Rank =
(25 − 18) / (42 − 18) × 100 ≈ **29** — closer to the low end of its own range. An IVR of 29 says
IV is *below-average* for this specific stock, which biases you toward *buying* options (debit
strategies) rather than selling.

**IV Percentile (IVP)** — the fraction of trading days in the past year on which IV was *lower*
than today's. If IV has been below 25% on 60% of days this year, IVP = **60**. IVP is more robust
than IVR to a single outlier spike (one panic day sets the 52-week high and distorts IVR; IVP
looks at the whole distribution).

**The decision rule you will use everywhere:**

- **High IV rank/percentile (say, > ~50, and especially > 70)** → options are *expensive* in this
  name's terms → favor **premium-selling** strategies (credit spreads, iron condors, covered
  calls, cash-secured puts). You are selling something richly priced, betting IV mean-reverts down
  (you are short vega — module 01).
- **Low IV rank/percentile (say, < ~30)** → options are *cheap* → favor **premium-buying** or
  debit strategies (long calls/puts, debit verticals, calendars/diagonals that are long vega).

We do not have DEMO's full price history in the offline samples, so we cannot compute a *real*
IVR from the CSV alone — v2 of the tool adds that. In the notebook we build the intuition by
computing HV from a synthetic series and comparing it to the chain's IV, which is the same
rich-vs-cheap judgment in miniature.

> **Why the sample chains cannot give you a true IV Rank.** IVR/IVP require a *time series* of
> past IVs; each sample CSV is a single snapshot. Treat the DEMO/LOWVOL/HIGHVOL comparison as a
> *cross-sectional* rich/cheap read (this stock's IV vs. that stock's), and the HV-vs-IV
> comparison as the *forecast-vs-realized* read. Real IV Rank is a v2 feature.

---

## 3. Skew: why puts trade rich

In module 00 you noticed the DEMO chain does **not** show one IV across all strikes: the 65 put
carried IV ~0.39 while the 105 call showed ~0.256. That strike-by-strike variation in IV is
**skew** (or the "volatility smile/smirk"). In equity indices and most single stocks the pattern
is a **put skew**: **out-of-the-money puts carry higher IV than equidistant OTM calls.** Downside
protection is bid up.

Why? Two durable reasons. First, **crash risk is asymmetric** — stocks fall faster and more
violently than they rise ("up the stairs, down the elevator"), so the market prices more tail
risk into downside strikes. Second, **structural demand for protection** — portfolio managers
constantly buy OTM puts as insurance and finance them by selling OTM calls, bidding put IV up and
pressing call IV down. The result is a persistent smirk: the DEMO chain's IV falling from ~0.39 at
the 65 put to ~0.246 in the far calls is a textbook equity put skew.

**Why you care as a strategist:** skew is *tradeable structure*, not noise. Because OTM puts are
richer, put-side premium selling (cash-secured puts, put credit spreads, the put wing of an iron
condor) collects *more* premium than the symmetric call side — you are paid extra for taking the
side the market fears. It is also why **risk reversals** and **broken-wing** structures (module 07)
exist: they exploit the price difference between the rich put wing and the cheap call wing. For
now, internalize the shape and *look for it in every chain you open.*

---

## 4. Term structure: IV across expirations

Skew is IV across *strikes* at one expiration. **Term structure** is IV across *expirations* at
one strike (usually ATM). Plot ATM IV against DTE and you get the vol term structure, and it
usually takes one of two shapes:

- **Contango (upward-sloping)** — longer-dated IV > shorter-dated IV. The normal, calm-market
  state: near-term is quiet, uncertainty accumulates further out.
- **Backwardation (downward-sloping)** — shorter-dated IV > longer-dated IV. A *stress* signal:
  the market is pricing acute near-term risk (an imminent event, a selloff) that it expects to
  resolve, so front-month vol spikes above the back.

The DEMO chain is mildly **backwardated** at the money — ATM IV runs ~0.269 at 7 DTE down to
~0.253 at 180 DTE. That front-loaded vol is the fingerprint of some near-term event risk priced
in. Term structure matters because **calendar and diagonal spreads (module 06) are trades on term
structure**: you sell the richer front-month vol and buy the cheaper back-month, wanting the shape
to normalize. Reading term structure tells you *which expiration* to sell and which to own.

---

## 5. Event vol and the crush

The most dramatic, most exploitable, and most dangerous volatility phenomenon retail traders meet
is **event volatility around earnings** (and FDA rulings, product launches, macro prints). Here is
the anatomy:

**Before the event**, uncertainty is high and known-to-be-imminent, so **IV inflates** — sometimes
enormously. A stock that normally carries 30% IV might see its front-week IV balloon to 70%+ the
day before earnings. The term structure goes sharply **backwarded** (the expiration bracketing the
event spikes far above later ones). Options get *expensive* precisely because everyone knows a big
move is coming.

**After the event**, the uncertainty *resolves in an instant.* The stock gaps to its new level and
the reason for the elevated IV vanishes. IV **collapses** — often from 70% back to 30% in a single
session. This is the **volatility crush** (or "vol crush"), and it is the number-one way
inexperienced traders lose money being *right*: you buy a straddle before earnings, the stock moves
exactly as much as you hoped, but the IV crush deflates both your legs so hard that your positive
delta gain is swamped by your vega loss. The event *has to* move the stock *more than the IV
already priced in* — the **implied move** — for a long premium trade to win.

**The implied (expected) move** is your ruler here. The market's own straddle price tells you how
big a move it is pricing: a rough one-standard-deviation move is `spot × IV × √(t)` (this is
exactly `analyzer.expected_move`), and the ATM straddle price is a close practical proxy. If the
DEMO ATM straddle for the event-week is ~7 points, the market is pricing a ~7% move. A long
straddle only profits if the stock moves *more than that*; a short straddle profits if it moves
*less* (and collects the crush). **Trading earnings is trading whether realized will exceed
implied — direction is almost secondary.** For most learners the durable lesson is defensive:
**know when earnings are, and do not accidentally hold long premium into a vol crush.** Deliberate
event trading is a module-08 topic; not getting blindsided is a today topic.

---

## 6. IV as THE strategy-selection input

Everything above collapses into one pre-trade habit. Before you pick *any* structure, you locate
yourself on two axes: **direction** (bullish / bearish / neutral) and **IV level** (high / low, in
the name's own terms). Direction you have opinions about from the start. The IV axis is the one
this module exists to install, because it flips which *expression* of your view is smart:

| Your directional view | IV is **LOW** (rank < ~30) | IV is **HIGH** (rank > ~50) |
|---|---|---|
| Bullish | buy: long call, **debit** call spread | sell: **cash-secured put**, put **credit** spread |
| Bearish | buy: long put, **debit** put spread | sell: **call credit** spread |
| Neutral | own theta cheaply: **calendar** (long vega) | sell premium: **iron condor / strangle** |

Read the two columns. **The same bullish opinion is a long call when IV is cheap and a
cash-secured put when IV is rich.** Buying options in high IV and selling them in low IV are both
uphill battles — you overpay for vega going in, or you undercollect for it. Matching the *sign of
your vega* to the *IV regime* is what "let IV pick the strategy" means, and it is the connective
tissue for every strategy module that follows (03, 04, 05). Do not skip it: a trader who reads IV
correctly but picks a mediocre structure usually beats one who picks the perfect structure in the
wrong IV regime.

---

## Key takeaways

- **HV is realized (backward); IV is implied (forward).** IV is the market's price of future
  movement; you back it out of the option price (`pricing.implied_vol`). Buying options bets
  realized > implied; selling bets realized < implied.
- **IV is meaningful only relative to the stock's own history.** Use **IV Rank** and **IV
  Percentile**: high (> ~50) → sell premium (short vega); low (< ~30) → buy premium (long vega).
  A single absolute IV number tells you almost nothing.
- **Skew**: OTM puts trade at higher IV than equidistant calls (crash-risk asymmetry + protection
  demand). It is tradeable structure — put-side selling is paid more.
- **Term structure**: ATM IV across expirations — contango (calm, upward) vs. backwardation
  (stress, front-loaded). Calendars/diagonals trade it.
- **Event vol & the crush**: IV inflates before earnings and collapses after. Long premium can
  *lose while right* if the move is smaller than the implied move. Know your earnings dates.
- **IV is the master input**: direction × IV level chooses the *expression* of your view. Same
  opinion, opposite structure depending on whether vol is rich or cheap.

## In the next module

Phase 2 begins. We start building real positions: **single-leg options and stock combinations** —
long calls and puts, covered calls, cash-secured puts, protective puts, and collars — each as a
full strategy card telling you exactly when its direction-and-IV profile fits.
