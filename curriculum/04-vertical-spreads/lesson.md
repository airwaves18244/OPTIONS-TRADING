# 04 — Vertical Spreads: Defined-Risk Directionality

A single long option has one problem you felt in module 03: you pay for time and vol you may not
need, and theta grinds you the whole way. A single short option has the opposite problem: you
collect premium but carry *undefined* risk — a naked short call can lose without limit. The
**vertical spread** solves both. You trade *two options of the same kind and expiration at
different strikes* — one long, one short — and in doing so you **define your risk**, **cheapen your
directional bet**, and **choose exactly how much probability to trade for how much reward.** After
this module you will express any directional view four ways and know which one the IV regime wants.

"Vertical" just means the two strikes sit in the same expiration column, stacked vertically on the
chain. There are four, and they pair up: two **debit** verticals (you pay) and two **credit**
verticals (you collect); two **bullish** and two **bearish**. The deep lesson is that **the same
directional opinion has a debit expression and a credit expression, and IV decides which is
smart.**

All examples on **DEMO**: spot **$100**, IV **~25%**, **45 DTE**, real chain mids.

---

## The mechanics all four share

Every vertical is *long one strike, short another, same kind, same expiry*. That structure forces
three things:

1. **Defined risk and defined reward.** Both max profit and max loss are fixed and known at entry.
   No tail. This is the single biggest reason spreads are the retail workhorse.
2. **Width sets the scale.** The distance between strikes (the **width**) times 100 is the total
   dollars "in play" for one spread. A 100/110 spread has a $1,000 width; max profit + max loss
   always sum to that width (minus nothing — they *are* the width). Wider = bigger bet, bigger risk
   and reward; narrower = smaller.
3. **Debit vs. credit is a mirror, not a different animal.** A bull *call* spread (debit) and a
   bull *put* spread (credit) both profit when the stock rises — they are two ways to be bullish
   with nearly identical payoff shapes. Which you choose is an **IV decision** (below), not a
   direction decision.

Two formulas you will use constantly (per share; ×100 for dollars):

- **Debit vertical:** max loss = debit; max profit = width − debit; breakeven = long strike ±
  debit (+ for calls, − for puts).
- **Credit vertical:** max profit = credit; max loss = width − credit; breakeven = short strike ±
  credit (− for put spreads, + for call spreads).

Notice the beautiful symmetry: for a bull call and the "same" bull put, max-profit and max-loss
roles simply swap. The debit spread pays a small debit to *win the width*; the credit spread
collects a small credit and *risks the width*.

---

## Debit vs. credit as an IV decision

This is the crux of the module. You are bullish on DEMO. You can buy a **bull call spread** (debit)
or sell a **bull put spread** (credit). Both make money if the stock rises. What's different is
their **vega**:

- A **debit** vertical is (slightly) **long vega** and **short theta** — you *paid* for net
  optionality. It wants IV to be **low** at entry (so you don't overpay) and benefits if IV rises.
- A **credit** vertical is (slightly) **short vega** and **long theta** — you *sold* net
  optionality. It wants IV to be **high** at entry (so you collect fat premium) and benefits as IV
  mean-reverts down and time passes.

So the rule, straight from module 02: **in low IV, express directional views with debit spreads;
in high IV, express them with credit spreads.** Bullish + low IV → bull call spread. Bullish + high
IV → bull put spread. Bearish + low IV → bear put spread. Bearish + high IV → bear call spread. The
matrix from module 02 was pointing here the whole time.

There is also a *probability* difference that follows from where you place the strikes. Debit
spreads are usually built *around or through* the money (you need a move to profit) → lower
probability, higher reward. Credit spreads are usually built *out of the money* (you profit if the
stock merely stays away from your short strike) → **higher probability of profit, lower reward.**
That trade-off — POP vs. max profit — is the other dial this module teaches.

---

## Strategy card — Bull Call Spread (debit)

**Construction.** Buy a lower-strike call, sell a higher-strike call, same expiry. On DEMO: buy the
100 call for **3.91**, sell the 110 call for **0.73** → net **debit 3.18** ($318). Width 10.
`strategies.bull_call_spread((100, 3.91), (110, 0.73), expiry=45/365)`.

**Payoff & greeks profile.** Max loss = debit = **$318** (stock ≤ 100 at expiry). Max profit =
width − debit = 10 − 3.18 = **$682** (stock ≥ 110). Breakeven = 100 + 3.18 = **103.18**. Net
**long delta** (bullish, ~+0.33), small **long vega**, modest **short theta** — the sold 110 call
pays back much of the lone call's decay and vega drag.

**When to use it.** Direction: **moderately bullish** — you expect a move to a target (≈ the short
strike) but not a moonshot. IV: **low** (debit structure prefers cheap vol). Horizon: 30–60 DTE for
a swing.

**Entry criteria.** Long strike near where you expect to be / the money; short strike at your
*price target* (you cap gains there, so put it where you think the stock lands or slightly beyond).
Width by risk appetite. Prefer to pay **≤ ~50–60% of the width** as debit so reward ≥ risk.
Liquidity on *both* legs.

**Management & adjustment.** Take profit at a target (e.g., **50–75% of max profit**) rather than
squeezing the last few dollars as gamma/pin risk rises near expiry. If wrong, the defined loss is
your stop — but consider cutting before full loss if the thesis breaks. You can *roll up* the whole
spread if the stock runs past your short strike and you want to keep participating.

**Exit rules.** Close by ~21 DTE if it hasn't worked (decay/gamma turn hostile); bank winners
early; let defined max loss cap the downside.

**Common mistakes.** Paying too much of the width as debit (poor reward/risk); setting the short
strike below a realistic target (capping gains too soon); buying debit spreads in *high* IV (you
overpay and fight vega); and treating the capped upside as unlimited.

---

## Strategy card — Bear Put Spread (debit)

**Construction.** Buy a higher-strike put, sell a lower-strike put, same expiry. On DEMO: buy the
100 put for **3.42**, sell the 90 put for **0.62** → net **debit 2.80** ($280). Width 10.
`strategies.bear_put_spread((100, 3.42), (90, 0.62), expiry=45/365)`.

**Payoff & greeks profile.** Max loss = debit = **$280** (stock ≥ 100). Max profit = width − debit
= 10 − 2.80 = **$720** (stock ≤ 90). Breakeven = 100 − 2.80 = **97.20**. Net **short delta**
(bearish, ~−0.33), small long vega, modest short theta. The bullish card, pointed down.

**When to use it.** Direction: **moderately bearish** toward a downside target. IV: **low** (debit)
— though remember the put skew makes downside optionality structurally pricier, so quantify the
debit. Horizon: 30–60 DTE.

**Entry criteria.** Long put near the money; short put at your downside target. Same "pay ≤ ~half
the width" guideline. Selling the lower put partly offsets the skew-inflated cost of the long put —
one reason a *spread* is often smarter than a lone put on the downside.

**Management & adjustment.** Bank at 50–75% of max profit; roll *down* if the stock craters past
your short strike and you want to keep riding; defined loss is the stop. Close by ~21 DTE if it
hasn't worked.

**Exit rules.** As the bull call spread, mirrored: profit target, ~21-DTE time stop, defined-loss
floor.

**Common mistakes.** Overpaying for the skew-rich long put (a lone put is often *worse*; the spread
helps); short strike too close (tiny reward); buying in high IV.

---

## Strategy card — Bull Put Spread (credit)

**Construction.** Sell a higher-strike put, buy a lower-strike put (protection), same expiry. On
DEMO: sell the 95 put for **1.58**, buy the 90 put for **0.62** → net **credit 0.96** ($96). Width
5. `strategies.bull_put_spread((95, 1.58), (90, 0.62), expiry=45/365)`.

**Payoff & greeks profile.** Max profit = credit = **$96** (stock ≥ 95 at expiry — both puts expire
worthless, keep the credit). Max loss = width − credit = 5 − 0.96 = **$404** (stock ≤ 90).
Breakeven = 95 − 0.96 = **94.04**. Net **positive delta** (bullish), **positive theta** (time is
your friend), **short vega** (falling IV helps). This is the bullish *credit* trade — you win if
DEMO rises, sits still, *or even drifts down a little*, as long as it stays above 95.

**When to use it.** Direction: **neutral-to-bullish** — you don't need a rally, just an absence of a
selloff below your short strike. IV: **high** (credit structure wants rich premium). Horizon: 30–45
DTE (the theta sweet spot). The put skew *helps* you — you're selling the rich put wing.

**Entry criteria.** Short strike selection is the key lever: a common professional default is a
**~30-delta short put** (or ~16-delta for a higher-probability, lower-credit version). Lower short
strike = higher POP, smaller credit; closer = fatter credit, lower POP. Aim to collect **~⅓ of the
width** as credit (here 0.96 on a 5-wide ≈ 19%; a 30-delta strike typically gets you nearer ⅓).
Buy the long wing as cheap disaster insurance that defines the risk.

**Management & adjustment.** The iron rule of credit spreads: **take profit at ~50% of max credit.**
Here that's buying it back for ~0.48 to lock ~$48 — you give up half the theoretical profit to
remove risk and free capital, and win far more consistently. If the stock falls and the short strike
is **tested** (spot near 95), your choices are: close for the defined loss, or **roll down and out
for a credit** (module 09 covers this in depth) if your thesis holds. Set a loss trigger — many
traders exit at **~2× the credit received** (~$192 loss here) rather than risking full max loss.

**Exit rules.** 50% profit target, or the ~2× credit loss stop, or defined max loss as the backstop.
Do not carry short spreads into the final week untended — gamma risk near the short strike spikes.

**Common mistakes.** Chasing fat credits by selling too-close short strikes (low POP, big losses);
holding for the last 50% of profit and getting run over (the 50% rule exists for a reason); not
having a loss trigger; selling credit spreads in *low* IV (thin credit, poor compensation).

---

## Strategy card — Bear Call Spread (credit)

**Construction.** Sell a lower-strike call, buy a higher-strike call (protection), same expiry. On
DEMO: sell the 105 call for **1.85**, buy the 110 call for **0.73** → net **credit 1.12** ($112).
Width 5. `strategies.bear_call_spread((105, 1.85), (110, 0.73), expiry=45/365)`.

**Payoff & greeks profile.** Max profit = credit = **$112** (stock ≤ 105 at expiry). Max loss =
width − credit = 5 − 1.12 = **$388** (stock ≥ 110). Breakeven = 105 + 1.12 = **106.12**. Net
**negative delta** (bearish), **positive theta**, **short vega**. The bearish *credit* trade: you
win if DEMO falls, sits, or rises only up toward your short strike.

**When to use it.** Direction: **neutral-to-bearish** — you don't need a crash, just no rally
through your short strike. IV: **high**. Horizon: 30–45 DTE. Note the call side sits on the
*cheaper* (lower-IV) wing thanks to skew, so credits are a bit thinner than the equivalent put
spread — a real consideration.

**Entry criteria.** ~30-delta short call as a default; further OTM for higher POP/less credit. Aim
for ~⅓-of-width credit. Buy the higher call to define risk. This is the classic call-side of an
iron condor (module 05).

**Management & adjustment.** Same iron rule: **50% profit target**; ~2× credit loss stop; **roll up
and out for a credit** if the short strike is tested and the thesis holds. Watch **early assignment
on the short call** if DEMO pays a dividend and the call goes deep ITM near ex-date (module 00).

**Exit rules.** 50% profit, ~2× credit stop, defined-loss backstop, off before the final-week gamma.

**Common mistakes.** Selling too close for a fat credit; ignoring dividend/early-assignment risk on
the short call; no loss trigger; selling into low IV.

---

## POP vs. max profit: the dial you set with strike selection

Here's the trade-off that governs every credit spread. Take the bull put spread and slide the short
strike:

- Short the **95** put (≈30-delta): collect ~0.96, POP ≈ 70%, risk $404 to make $96.
- Short the **90** put (≈16-delta): collect less (~0.40 net on a 5-wide), POP ≈ 84%, but a smaller
  credit and worse reward-to-risk.
- Short the **97.5** put (near 40-delta): collect more, POP drops toward ~60%, credit fattens.

**You cannot have both high POP and high reward** — the market prices them against each other. A
16-delta short strike wins ~84% of the time but pays little and loses a lot on the rare miss; a
40-delta strike pays well but loses more often. The "right" spot is a *risk-management* choice, not
a math trick: most premium sellers live around the **30-delta short strike** as a balance and
enforce discipline with the **50%-profit / defined-loss** rules. The notebook plots POP against
max profit across short strikes so you can *see* the frontier and pick your point on it.

---

## POP is not edge: the expectancy check

One more thing before you fall in love with high-probability credit spreads. A **70% POP does not
mean the trade is good** — it means you win 70% of the time. Whether that is *profitable* depends on
how much you win versus how much you lose. The number that matters is **expectancy**:

```
expectancy ≈ (POP × average win) − ((1 − POP) × average loss)
```

Take the DEMO bull put spread: POP ≈ 70%, but you risk **$404** to make **$96**. Plug in the raw
max values as a rough bound: (0.70 × 96) − (0.30 × 404) = 67.2 − 121.2 = **−$54**. On those crude
numbers the trade *loses* money over time — the fat loss on the 30% of misses swamps the thin wins.
This is the trap of naked high-POP selling: the market prices POP and payoff against each other
(the frontier you just saw), so a high win rate is *paid for* with a punishing loss ratio.

What rescues the credit spread is **management, not the entry odds.** Taking profit at **50%** cuts
the average win's *time and risk* (raising annualized expectancy and win consistency), and a loss
trigger at **~2× credit** caps the average loss well below the theoretical max — turning that −$54
back positive in practice. The lesson to carry into module 05: *never* judge a premium-selling trade
by POP alone. Always ask "what do I win, what do I lose, and how will I manage each?" A 70% POP with
an unmanaged 4:1 loss ratio is a slow-motion account bleed; the same trade managed at 50%/2× is a
sound, repeatable edge.

## Key takeaways

- A vertical is **long one strike, short another, same kind and expiry** — it **defines risk and
  reward**, cheapens the directional bet, and lets you dial probability vs. payoff. Max profit +
  max loss = the **width**.
- **Debit verticals** (bull call, bear put): pay a debit, **long-vega/short-theta**, built near/through
  the money → lower POP, higher reward. Use in **low IV**.
- **Credit verticals** (bull put, bear call): collect a credit, **short-vega/long-theta**, built OTM
  → **higher POP**, lower reward. Use in **high IV**.
- **The same direction has a debit and a credit expression** — IV picks which: bullish + low IV =
  bull call; bullish + high IV = bull put. This is module 02's matrix made concrete.
- **Credit-spread management is a discipline**: default to a **~30-delta short strike**, collect
  **~⅓ of the width**, **take profit at 50%**, set a ~2× loss trigger, and be *off before the
  final-week gamma*. Roll tested spreads down/up-and-out *for a credit* only if the thesis holds.
- **POP and max profit trade off** via strike selection — you cannot maximize both; choose your
  point on the frontier deliberately.

## In the next module

Combine a bull put and a bear call and you've sold *both* sides of a range: the **iron condor**.
Module 05 builds the neutral, premium-selling income structures — straddles, strangles, condors,
butterflies — where expected move, delta-based strike selection, and gamma risk near expiry take
center stage.
