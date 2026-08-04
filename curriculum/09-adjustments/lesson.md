# 09 — Adjustments: Tuning Open Positions When the Market Changes

Everything until now was about *opening* a good position. This module is about the harder, more
valuable skill: what to do when the market moves against one you already hold. Most traders have no
plan for this moment, so they freeze, hope, and then close at the worst possible time. You will do
better. An adjustment is a deliberate second trade layered onto the first to change its risk — to buy
time, to move a strike out of harm's way, to flatten a runaway delta, or to cap a loss. Done well, it
turns a losing position into a smaller loss, a scratch, or occasionally a win. Done badly, it throws
good money after bad and *increases* risk into a thesis that is already wrong. The difference is a
framework, and this module is that framework. It is the reason the analyzer's `scenario_grid` exists:
you replay the adverse move, then test each candidate adjustment and *see* what it does to your P&L
surface, greeks, and probability of profit before you commit a dollar.

---

## The first question is always: adjust or close?

Before any roll, hedge, or clever repair, answer one question honestly:

> **Is the original thesis still intact?**

An adjustment only makes sense if the reason you put the trade on is *still true* and the market has
simply moved faster, further, or sooner than expected. If the thesis is **broken** — you were bullish
and the company guided down, you were selling a range and the range broke on real news, you were
neutral and a trend started — then **close**. Adjusting a dead thesis is the single most expensive
mistake in options: you are adding capital and risk to a bet you would no longer make fresh. The test
is brutal and clarifying: *with what I know now, at these prices, would I open this position today?*
If no, do not "adjust" it — exit and redeploy.

If the thesis **is** intact, adjusting is on the table. Then a second filter:

- **Can I adjust for a credit (or at worst a tiny debit)?** The iron rule of rolling (below) is that
  you roll for a *credit*. Paying a large debit to defend usually just enlarges max loss.
- **Does the adjustment improve my risk, not just my feelings?** Measure it. A "repair" that widens
  max loss or flips you to undefined risk is not defense — it is doubling down. The notebook makes
  you check `max_loss`, greeks, and POP before/after.
- **Am I still within my sizing?** If defending would push the position past your per-trade risk
  limit (module 10), the answer is close, not add.

Three honest outcomes exist, and only two involve staying in: **close** (thesis broken, or defense is
not worth it), **adjust** (thesis intact, credit-neutral defense improves risk), or **do nothing**
(the position is tested but still inside plan — not every wiggle needs a trade; over-adjusting bleeds
you with commissions and slippage).

---

## Rolling: the core adjustment verb

To **roll** is to close an existing option leg and simultaneously open a similar one at a different
strike and/or expiration. It is one order (a spread) so you cross the market once. Three directions:

### Roll out (time)

Close the near leg, open the same strike further out in time. This **buys time** for the thesis and,
because a longer-dated option has more extrinsic value, a roll out to a further expiry almost always
collects a **credit**. You use it when the trade needs more room to work and the strike is still fine.
The cost is duration: you are now committed longer, and capital is tied up.

### Roll up / roll down (strikes)

Close the current strike, open a nearer or further one. **Roll down** a tested short put (move the
short strike lower, away from the falling price) to reduce the chance of assignment and cut delta;
**roll up** a short call similarly on a rally. Rolling a strike *away* from the money reduces risk but
usually costs premium — which is why you almost always combine it with a roll *out* in time.

### Roll out-and-away (both)

The workhorse defensive roll: **out in time and away in strike, for a net credit.** Rolling out
enough in time funds the move of the strike away from the money, so the whole package still brings in
cash. Example: a tested 45-DTE short put at strike 95 with the stock at 92 → roll to a 75-DTE short
put at strike 90, collecting a credit. You have lowered your obligation strike, reduced delta, bought
seven-plus weeks, and got paid to do it. That is a textbook defensive adjustment.

### The roll-for-credit rule

**Never roll for a net debit to defend a losing position.** If the only roll available costs you
money, you are paying to increase or prolong risk — usually a sign the thesis is broken and you
should close instead. Rolling for a credit means the market is still paying you to hold the (adjusted)
risk; rolling for a debit means it is charging you, and you should listen. (Rolling a *winner* up to
take profit and re-establish is different — that is offense, not defense.) The rare exception is a
deliberate, small debit to convert undefined risk into defined risk, e.g., buying a wing — that is
buying insurance, not doubling down, and you size it as such.

---

## Defending tested credit spreads and iron condors

These are the bread-and-butter defenses because credit spreads and condors are the positions you hold
most as a premium seller. The pattern: one side gets **tested** (price approaches or breaches a short
strike). Options in order of aggressiveness:

### 1. Do nothing (yet)

If the short strike is merely approached and you are still before your management point (21 DTE, or
short delta still modest), often the best trade is none. Theta is on your side; a small pullback fixes
it. Reserve ammunition.

### 2. Roll the untested side toward the money — for a credit

The elegant condor defense. The *call* side is fine but the *put* side is tested. You **roll the
untested call spread down** (closer to the money), collecting additional credit. That new credit
**widens your breakeven** on the tested side and lowers your overall cost basis, without adding risk
on the side that is already in trouble. You are harvesting the profit sitting in the safe side to
subsidize the tested side. Keep rolling the untested side in as long as it keeps paying and does not
create a new problem (do not roll it so far it becomes the tested side). This is the highest-value,
lowest-risk condor adjustment and the one to reach for first.

### 3. Roll the tested side out-and-away

If rolling the untested side is not enough, roll the *tested* spread out in time and further away in
strike, for a credit, per the rules above. Now both the breakeven and the calendar are more forgiving.

### 4. Go inverted

When a short strangle/condor is deeply tested and the two shorts have been rolled until the tested
short passes *through* the untested short, you can end up **inverted** — e.g., a short put strike now
*above* the short call strike. An inverted strangle has a guaranteed intrinsic cost equal to the
inversion width, but if the total credit collected across all the rolls exceeds that width, the
position can still be closed for a net profit or scratch on a reversion. Inversion is an advanced,
last-ditch move for undefined-risk sellers; it is a way to keep collecting credit while you wait for
mean reversion. Know the max-loss math cold before using it.

### 5. Convert the breached side to a butterfly (cap the loss)

When one side of a condor or a credit spread is genuinely breached and rolling for a credit is no
longer available, you can **convert the tested vertical into a butterfly** by *buying* a further
option that turns the runaway short into the body of a fly. Concretely, a breached short put spread
(long lower put, short higher put) becomes a put butterfly when you buy a put below the long strike —
this **caps the max loss** at a defined, smaller number and even creates a profit tent if price
stalls near the short strike. It usually costs a small debit (buying the extra wing), and that is the
allowed exception to the credit rule: you are *buying a cap on catastrophe*. Converting to a fly is
how you say "this side is broken; I accept a defined, limited loss and stop the bleeding."

---

## Delta hedging: neutralizing directional drift

Any position accumulates delta as the underlying moves — a short put's delta grows as the stock
falls; a condor's net delta swings as one side is approached. **Delta hedging** is adding a position
whose delta offsets the drift, to bring the book back toward neutral when your view is still
range/vol-based rather than directional.

- **With stock/shares.** The cleanest hedge: if your position is +40 deltas long and you want flat,
  short 40 shares (each share is 1 delta). Precise, no added optionality, but uses buying power and,
  for shorts, borrow. Common for defending a tested short put on a name you do *not* want to own.
- **With options.** Buy or sell an option to inject the needed delta — e.g., buy a put to add
  negative delta against a position that has gone too long. This also changes your gamma/vega, which
  can be a feature (adding long gamma to a short-gamma condor near expiry) or a cost (paying theta).
- **How much, how often.** You do not hedge every delta every minute — that grinds you to death on
  costs. Hedge to a band (e.g., re-flatten when net delta exceeds ±X per your sizing), and remember a
  hedge is a *directional* trade layered on: if you are confident in the range, hedge; if you are now
  directional, maybe you should just take the directional position and close the original.

The key mental model: `position_greeks` gives you the current dollar delta; a hedge is whatever
offsets it to your target. Recheck greeks after every adjustment — that is the discipline this module
drills.

---

## The ~21-DTE decision point and gamma risk

Short-premium positions carry **negative gamma**: as expiry nears, delta changes faster and faster
for a given move, so a position that was calm at 45 DTE can lurch violently in its final two weeks.
The same theta that made near-dated selling attractive comes bundled with this gamma. The
professional convention: **make a decision at around 21 DTE.** By then you either:

- **Take the winner off** (a credit spread/condor at 21 DTE is usually near its profit target —
  close it and redeploy into a fresh 45-DTE cycle), or
- **Roll the whole position out** to the next cycle for a credit (buying time and *reducing* gamma by
  moving to a longer-dated position), or
- **Close a loser** whose thesis is broken.

What you do **not** do is casually carry short gamma into the last week hoping — that is where a pin
or a gap turns a manageable position into a maximum loss overnight. "21 DTE" is a convention, not
magic; the real rule is *stop feeding negative gamma near expiry.* Calendars and pin trades have the
mirror problem (they *want* to be near the short strike at front expiry but hate being far from it),
so their 21-DTE decision is about whether the pin thesis is alive.

---

## Repair strategies for broken long positions

Directional longs go wrong too. Two classic repairs:

### The stock repair (1×2 call ratio overlay)

You own 100 shares that have dropped and you want to lower your break-even without adding much cash or
much downside risk. Overlay a **1×2 call ratio** in the direction of a bounce: buy one ATM call and
sell two further-OTM calls (often for near zero cost). If the stock recovers to the short strike, the
extra long call *doubles* your participation over that range, letting you exit near break-even on a
partial recovery instead of needing a full one. The trade-off: your upside is **capped** at the short
strike (you sold two calls, one naked against the stock, but the stock covers it, so it is really a
covered-call-plus-extra-long), and you gain nothing if the stock keeps falling. It is a repair for a
*moderate* bounce thesis, not a rescue for a broken company.

### Rolling a broken long call

A long call that has moved against you (stock fell, call is now OTM and bleeding theta) can be
**rolled down and out**: close the current call, buy a lower strike further in time, for a manageable
debit — but only if you still believe in the move. Often the cleaner repair is to **convert to a
spread** by selling a call against your long (turning the naked long into a debit spread), which
reduces theta bleed and lowers break-even at the cost of capped upside. As always: if the *reason* you
bought the call is gone, close it; repairs are for intact theses that need more time or a lower bar.

---

## Key takeaways

- **Adjust only when the thesis is intact.** If you would not open the position fresh today, close it
  — do not "defend" a broken bet.
- **Roll for a credit.** Out (time) buys room and pays; away (strike) reduces risk; **out-and-away**
  does both for net cash. A debit-only roll is the market telling you to close.
- **Defend condors by rolling the *untested* side in for a credit first** — it subsidizes the tested
  side without adding risk there. Then roll the tested side out-and-away; then invert; then convert
  the breached side **to a butterfly** to cap the loss (the allowed small-debit exception).
- **Delta-hedge with stock or options** to offset directional drift when your view is still
  range/vol-based — hedge to a band, and recheck greeks after every change.
- **Make a decision at ~21 DTE.** Stop feeding negative gamma into expiration: take winners, roll, or
  close — never carry short gamma into the last week and hope.
- **Repair broken longs** with a 1×2 ratio (stock repair) or by converting to a spread — only if the
  thesis lives. Every adjustment is measured: `max_loss`, `position_greeks`, and POP **before vs
  after**, or it is not an adjustment, it is a hope.

## In the next module

Adjustments keep individual trades alive; the next module is the professional wrapper around all of
them — position sizing, portfolio greek limits, liquidity and event rules, the journal and checklists,
and the psychology that decides whether you actually *follow* the framework you just learned.
