# 05 — Neutral Income: Trading a Range, Selling Volatility

Every strategy so far has had a directional lean. Now we take the lean out. This module is about
trading **magnitude, not direction** — positions that profit from the stock *staying inside a
range* (and from volatility falling), or, on the long side, from it *breaking out* of one. These
are the premium-seller's bread and butter: the **short strangle**, the **iron condor**, the **iron
butterfly** — plus their long-volatility mirrors (long straddle/strangle) and the surgical **long
butterfly**. After this module you can build a defined-risk range trade, place its short strikes by
delta, size its wings, target a credit, overlay the expected move on its breakevens, and — most
importantly — respect what gamma does to it near expiration.

This is where module 02 pays off hardest: these are, with one exception, **high-IV strategies.**
You sell them when implied volatility is rich and profit as it mean-reverts down while the stock
goes nowhere. Selling them in low IV is the classic beginner error — thin credit, same risk.

All examples on **DEMO**: spot **$100**, IV **~25%**, **45 DTE**. First, the ruler everything in
this module is measured against.

---

## The expected move: the ruler for range trades

The **expected move** is the market's own estimate of how far the stock will travel by
expiration — the one-standard-deviation (~68% probability) range. The formula (module 02, and
`analyzer.expected_move`) is:

```
expected_move = spot × IV × √t
```

For DEMO at 45 DTE: 100 × 0.25 × √(45/365) ≈ 100 × 0.25 × 0.351 ≈ **±8.8 points** → roughly a
91.2–108.8 range holds about 68% of the time. This number is the reference for *every* structure
below. A range trade's whole thesis is "the stock stays inside a range"; the expected move tells
you where the market thinks the edges are, so you can decide whether your breakevens sit **inside**
the expected move (higher credit, lower probability — you're betting on *less* movement than
priced) or **outside** it (lower credit, higher probability — you're betting the stock is calmer
than 1σ). Overlaying the expected move on a payoff diagram is the single most useful sanity check
in neutral trading, and the notebook does exactly that on an iron condor.

---

## Strategy card — Long Straddle

**Construction.** Buy the ATM call *and* the ATM put, same strike, same expiry. On DEMO: buy the
100 call (**3.91**) and the 100 put (**3.42**) → **debit 7.33** ($733).
`strategies.long_straddle((100, 3.91), (100, 3.42), expiry=45/365)`.

**Payoff & greeks profile.** A "V" — you profit from a **big move in either direction**. Max loss
= the debit, **$733**, if the stock pins exactly at 100 at expiry (both legs worthless). Profit is
open-ended on both sides beyond the breakevens = strike ± debit = **92.67 and 107.33**. Greeks:
**delta ≈ 0** (neutral at entry), **long gamma** (a move helps, accelerating), **long vega**
(rising IV inflates both legs), **short theta** (you pay decay on *two* long options — brutal).

**When to use it.** Direction: **none** — you expect a *large* move but don't know which way (a
binary event, a breakout). IV: **low** — critically, you need IV *cheap* going in, because a long
straddle is doubly long vega and gets destroyed by a vol crush. Buying a straddle into elevated
pre-earnings IV is the number-one way to be right on the move and still lose (module 02). Horizon:
match the catalyst.

**Entry criteria.** ATM strike. The stock must move **more than the debit** (here 7.33, ~7.3%) just
to break even — compare that required move to the **expected move** (8.8): if the debit's implied
move is *less* than what you think the stock will actually do, the trade has an edge. Buy time so
theta doesn't gut you before the catalyst.

**Management & adjustment.** Take profit into a sharp move (the winning leg's gamma has done its
work; remaining extrinsic is decay risk). If the move happens, consider closing the losing leg for
scraps and riding the winner, or take the whole thing off. Don't let a straddle bleed theta waiting.

**Exit rules.** Event-driven: exit right after the catalyst resolves (before the vol crush eats
you), or on a time stop if the move never comes.

**Common mistakes.** Buying into high IV (crush); underestimating the double theta bleed;
needing too big a move to clear a fat debit; holding through the event expecting more.

---

## Strategy card — Short Straddle

**Construction.** The mirror: **sell** the ATM call and ATM put. On DEMO: sell the 100 call
(3.91) and 100 put (3.42) → **credit 7.33** ($733). `strategies.short_straddle((100, 3.91),
(100, 3.42), expiry=45/365)`.

**Payoff & greeks profile.** An inverted "V" — you profit if the stock **sits still**. Max profit
= the credit, **$733**, at a pin at 100. Loss is **theoretically unlimited** (undefined) beyond
the breakevens 92.67 / 107.33 — this is a naked, undefined-risk position. Greeks: **delta ≈ 0**,
**short gamma** (a move hurts, accelerating — the seller's curse), **short vega** (falling IV
helps), **positive theta** (you collect decay on two options). The purest *delta-neutral,
short-vega, positive-theta* trade there is (module 01).

**When to use it.** Direction: **neutral**, expecting a *quiet* stock. IV: **high** — you want to
sell rich premium and harvest the crush. Horizon: 30–45 DTE, managed early. **This is an advanced,
undefined-risk trade** — most retail traders should prefer its *defined-risk* cousin, the iron
butterfly (below), which caps the tails.

**Entry criteria.** Sell into elevated IV rank; collect a credit that comfortably exceeds the
expected move if you can. Size *tiny* — undefined risk means one gap can be ruinous.

**Management & adjustment.** **Take profit at ~25% of max credit** (short straddles are managed
tighter than spreads because the risk is undefined and gamma is vicious). Defend a tested side by
rolling the untested option closer (turning it into a strangle), or roll out in time for a credit.
Be **off well before the final two weeks** — short-gamma near expiry is where accounts die.

**Exit rules.** 25% profit target; a hard loss stop (e.g., ~1–2× the credit); mandatory time exit
around 21 DTE.

**Common mistakes.** Trading it undefined-risk in size; selling into low IV; holding into
expiration for the last dollars while short gamma explodes; no loss stop on an unlimited-loss
trade.

---

## Strategy card — Long / Short Strangle

**Construction.** Like the straddle but with **OTM** strikes, cheaper and wider. **Long strangle**
(DEMO): buy the 95 put (**1.58**) and 105 call (**1.85**) → **debit 3.43** ($343).
`strategies.long_strangle((95, 1.58), (105, 1.85), expiry=45/365)`. **Short strangle**: sell the
same two → **credit 3.43**. `strategies.short_strangle((95, 1.58), (105, 1.85), expiry=45/365)`.

**Payoff & greeks profile.** Same shapes as the straddle, but with a **flat bottom (long) / flat
top (short)** between the strikes instead of a single point. Long strangle breakevens = 95 − 3.43
and 105 + 3.43 = **91.57 / 108.43**; max loss = debit ($343) anywhere between 95 and 105. Short
strangle: max profit = credit ($343) anywhere between the strikes; **undefined loss** beyond the
breakevens. Greeks mirror the straddle (long/short gamma, long/short vega, short/long theta) but
*muted* — OTM options have less gamma and vega than ATM, so the strangle is gentler and cheaper.

**When to use it.** Long strangle: neutral-direction, **big-move** bet, **low IV**, when you want a
cheaper entry than the straddle (at the cost of needing a bigger move). Short strangle:
neutral, **quiet-stock** bet, **high IV** — the higher-probability, wider-margin cousin of the
short straddle (the flat top gives room before you're tested). Horizon 30–45 DTE.

**Entry criteria.** Delta-based strike selection is the professional habit: sell the **~16-delta
put and ~16-delta call** (roughly the 1σ strikes) for a short strangle — that places your short
strikes near the edges of the expected move, giving ~68–70% POP. On DEMO those are near the 90 put
/ 110 call; the 95/105 version above sits closer to ~30-delta (fatter credit, lower POP).

**Management & adjustment.** Short strangle: **take profit at ~50% of credit** (a bit looser than
the straddle since it's wider); defend the tested side by rolling the untested side toward it for
more credit; roll out in time for a credit if needed; off before the last two weeks. Long strangle:
take profits into a move, time-stop if it doesn't come.

**Exit rules.** As above — 50% profit (short), event/time driven (long), hard stops on the
undefined-risk short.

**Common mistakes.** Same family as the straddle: wrong IV regime, undefined-risk sizing on the
short, holding into gamma. Selling strangles too close (30-delta or tighter) chasing credit and
getting tested constantly.

---

## Strategy card — Iron Condor (the flagship range trade)

**Construction.** A short strangle with **defined risk** — sell an OTM put spread *and* an OTM call
spread, same expiry. Four legs, ascending strikes. On DEMO: long 90 put (**0.62**), short 95 put
(**1.58**), short 105 call (**1.85**), long 110 call (**0.73**) → net **credit 2.08** ($208).
`strategies.iron_condor((90, 0.62), (95, 1.58), (105, 1.85), (110, 0.73), expiry=45/365)`.

**Payoff & greeks profile.** A flat-topped tent: you keep the full credit if the stock finishes
**between the short strikes (95–105)**, with defined losses beyond. Max profit = credit = **$208**.
Max loss = wing width − credit = 5 − 2.08 = **$292** per side (you can only lose on one side at
expiry). Breakevens = 95 − 2.08 and 105 + 2.08 = **92.92 / 107.08**. Greeks: **delta ≈ 0**
(neutral), **short gamma**, **short vega** (profits as IV falls), **positive theta** (collects decay)
— the short strangle's profile, but with the tails **capped** by the long wings.

**When to use it.** Direction: **neutral**, expecting the stock to stay range-bound. IV: **high**
IV rank — this is *the* strategy to deploy when a name's IV is elevated and you expect it to calm.
Horizon: 30–45 DTE (theta-rich, gamma still manageable). The flagship because it packages the whole
"sell volatility, defined risk" thesis into one order.

**Entry criteria.** Place the **short strikes by delta** — a common default is **~16-delta shorts**
(near the 1σ / expected-move edges, ~70% POP) or ~30-delta for more credit/less probability. Then
choose **wing width**: wider wings = more credit but more risk per side; narrower = cheaper
insurance, less credit, better reward-to-risk. Target a **credit of about ⅓ of the wing width** as
a rule of thumb (here 2.08 on a 5-wide is generous because the shorts are near 30-delta). Compare
the breakevens to the expected move: ideally your short strikes sit at/beyond the expected-move
edges.

**Management & adjustment.** **Take profit at ~50% of max credit** — the iron rule again. Defend a
**tested side** (say the stock falls toward 95) by **rolling the *untested* call spread down** for
more credit (narrowing your range but improving the credit/breakeven on the threatened side), or
roll the tested side out and away for a credit — all covered in depth in module 09. Set a loss
trigger (e.g., ~2× credit, or when a short strike goes ITM). **Gamma risk near expiry** is the
condor's defining hazard: as expiration nears with the stock pinned near a short strike, small
moves swing P&L violently — manage the position *off* by ~21 DTE rather than gambling on the pin.

**Exit rules.** 50% profit target; ~2× credit loss stop; ~21-DTE time exit; never ride an untended
condor into the final week.

**Common mistakes.** Selling condors in **low IV** (thin credit, same risk — the cardinal sin);
short strikes too tight (constantly tested); wings so wide the risk dwarfs the credit; holding to
expiration through the gamma; and forgetting it's a *bet on quiet* — a trending stock is the
condor's enemy.

---

## Strategy card — Iron Butterfly

**Construction.** An iron condor whose short put and short call sit at the **same (ATM) body
strike** — a short straddle with defined-risk wings. On DEMO: long 90 put (**0.62**), short 100 put
(**3.42**), short 100 call (**3.91**), long 110 call (**0.73**) → net **credit 5.98** ($598).
`strategies.iron_butterfly((90, 0.62), (100, 3.42), (100, 3.91), (110, 0.73), expiry=45/365)`.

**Payoff & greeks profile.** A sharp tent peaked at the body. Max profit = credit = **$598**, but
*only if the stock pins exactly at 100* at expiry. Max loss = wing width − credit = 10 − 5.98 =
**$402** beyond the wings. Breakevens = 100 ± 5.98 = **94.02 / 105.98**. Because the shorts are ATM,
it collects a **much larger credit** than the condor but has a **narrower profit tent** and a
**lower probability** of hitting max profit. Greeks: delta ≈ 0, short gamma (sharper — ATM shorts),
short vega (large), positive theta (large).

**When to use it.** Direction: **neutral with a pin thesis** — you expect the stock to gravitate to
a specific price (often the current price). IV: **high** — the ATM shorts mean big vega, so you
want rich IV to sell and a crush to profit from. Horizon: 30–45 DTE. It's the defined-risk version
of the short straddle — prefer it over the naked straddle for the capped tails.

**Entry criteria.** Body at your pin target (usually ATM); wings set the width/risk. The large
credit (here ~60% of the 10-wide width) means a **wide breakeven range** (94–106) despite the
narrow max-profit point — you don't need a perfect pin to profit, just to land inside the
breakevens.

**Management & adjustment.** **Take profit at ~25% of max credit** (managed tighter than the condor
because the ATM short gamma is fierce). Defend by rolling the untested side or converting toward a
condor (rolling a short in). Off before the final-week gamma. A tested iron fly moves fast — respect
it.

**Exit rules.** 25% profit target; loss stop; ~21-DTE exit.

**Common mistakes.** Expecting to capture max profit (a perfect pin is rare — the trade is really
about landing inside the wide breakevens); underestimating the ATM short gamma; low-IV entry.

---

## Strategy card — Long Butterfly

**Construction.** A **long, defined-risk, low-cost pin bet**: buy 1 lower call, sell 2 middle
calls, buy 1 higher call (all calls, or all puts), equal wings. On DEMO: buy the 95 call
(**7.05**), sell two 100 calls (**3.91** each), buy the 105 call (**1.85**) → net **debit 1.08**
($108). `strategies.long_call_butterfly((95, 7.05), (100, 3.91), (105, 1.85), expiry=45/365)`.

**Payoff & greeks profile.** A tent, like the iron fly, but entered for a small **debit** instead
of a credit. Max profit = wing width − debit = 5 − 1.08 = **$392** at a pin at the middle strike
(100). Max loss = debit = **$108**, beyond the wings — a tiny, defined risk for a large potential
payoff (here ~3.6:1). Breakevens = 95 + 1.08 and 105 − 1.08 = **96.08 / 103.92** — a *narrow*
profit zone. Greeks near entry are small and mixed (it's a balanced structure); as expiry
approaches it becomes a concentrated bet on the middle strike.

**When to use it.** Direction: **neutral, precise pin thesis** — you think the stock lands very
near a specific price by expiration. IV: it's cheapest to *buy* a fly when IV is **low-to-moderate**
(the debit is smaller). Unlike the other structures here, a long butterfly is a **long-premium,
cheap-lottery-on-a-pin** trade rather than a rich-IV income trade — a useful contrast to internalize.
Horizon: it works best held closer to expiration, when the tent sharpens and the middle strike's
value peaks.

**Entry criteria.** Middle strike at your pin target; symmetric wings sized to the risk/reward you
want (wider wings = bigger max profit and wider profit zone, larger debit). Very low absolute cost
makes it easy to size, but the narrow profit zone means most expire near the small max loss —
size it as the small-probability, large-payoff bet it is.

**Management & adjustment.** Because max profit only materializes near expiration at a near-perfect
pin, many traders take a partial profit if the stock parks at the middle strike with time left
(the fly's value rises as expiry nears *if* price cooperates). Small defined loss is the stop — no
adjustment usually needed for such a cheap structure.

**Exit rules.** Hold toward expiration for the pin, or take profits if it's deep in the tent with
time left; let the small debit be the max loss.

**Common mistakes.** Expecting to routinely capture max profit (the profit zone is *narrow* — most
flies expire worthless or near it); putting the body where you *hope* rather than where the stock is
likely to land; oversizing because "it's cheap" (a cheap trade that usually loses its full debit
still adds up).

---

## Gamma risk near expiry: why range trades get managed early

Read across the short-premium cards and one warning repeats: **manage it off before the final one
or two weeks.** Here's the mechanism, from module 01. Short-premium structures are **short gamma**,
and gamma **explodes near expiration** for strikes near the money. Early in the trade, a $2 move in
DEMO barely dents a condor — the short strikes are far off and gamma is low. In the last week, with
the stock parked near a short strike, that same $2 move swings the position's delta and P&L
violently: your "delta-neutral" income trade suddenly has a big directional exposure that flips
sign as the stock oscillates around the strike. The **pin risk** at expiration (module 00) is the
extreme of this. That is why professional premium sellers harvest **50% (condor/strangle) or 25%
(straddle/iron fly)** of the credit and **exit around 21 DTE** rather than squeezing the last
dollars: the shrinking remaining profit is not worth the exploding gamma. The single discipline
that most separates surviving premium sellers from blown-up ones is *leaving the last bit on the
table.*

---

## Key takeaways

- Neutral trades bet on **magnitude, not direction**. The **expected move** (`spot × IV × √t`,
  ≈ ±8.8 on DEMO at 45 DTE) is the ruler: it tells you where the market prices the 1σ edges, so you
  can place breakevens inside (more credit, less probability) or outside (more probability, less
  credit) it.
- **Short premium = short gamma, short vega, positive theta** — these are **high-IV strategies**.
  Sell rich IV, profit as it mean-reverts and the stock sits. Selling them in low IV is the
  cardinal error.
- **Short strangle** (undefined risk) → **iron condor** (defined risk) is the workhorse pair;
  **short straddle** (undefined) → **iron butterfly** (defined) is the ATM, fatter-credit,
  narrower-tent pair. Prefer the **defined-risk** versions.
- **Place short strikes by delta** — **~16-delta** shorts sit near the expected-move edges (~70%
  POP); ~30-delta pays more with lower probability. Choose **wing width** for the risk/reward and
  target ~⅓-of-width credit on condors.
- **Long straddle/strangle** are the mirrors: long gamma, long vega, **short theta** — big-move
  bets for **low IV**, and lethal to hold through a vol crush. The **long butterfly** is a cheap,
  defined-risk *pin* bet with a narrow profit zone.
- **Manage early**: 50% profit (condor/strangle), 25% (straddle/iron fly), exit ~21 DTE. **Gamma
  near expiry** is the neutral trader's central hazard — leave the last bit on the table.

## In the next module (Phase 3)

You've built the core catalog. Phase 3 adds the **calendar and diagonal spreads** — trades across
*expirations* rather than strikes, where term structure (module 02) and mark-to-model P&L
(`pnl_at`, because the legs expire on different days) become essential — and then the framework for
choosing among *all* of it given a market regime.
