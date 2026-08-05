# 11 — Capstone: The 30-Day Paper-Trading Program

Knowledge you cannot execute under uncertainty is worth nothing in this game. This capstone converts
everything from modules 00–10 into a **30-day paper-trading program** with one deliverable that
graduates you: a **written trading plan**, backed by a journal of at least ten paper trades including
at least two you actively managed. You will trade a deliberate variety of structures, size every one
by the module-10 rules, journal daily, review weekly against your checklists, and finish by writing
the plan you will actually trade from. Paper trading is not the real thing — there is no true
slippage and no real fear — but done honestly (real prices, real sizing, real journaling, no
do-overs), it builds the *process* that survives contact with real money. Treat it as if it were
real; the whole point is to make the discipline automatic before dollars are on the line.

---

## How to run the program (rules of engagement)

- **Paper account, real prices.** Use a broker paper account or track against the sample chains /
  live mids. Record the price you *could* actually have gotten (the mid or worse), never the perfect
  fill.
- **Fixed sizing from day one.** Risk **1–2% of a stated (paper) account equity** per trade, sized by
  `analyzer.max_loss`. Pick your equity number (e.g., `$25,000`) and hold to it.
- **One or two new positions at a time.** This is a learning program, not a volume contest. Quality
  over quantity; every trade must pass the entry checklist.
- **Journal every trade** (module 10 template) at entry and exit, and write a **daily** note on every
  open position.
- **No untracked, unplanned trades.** If it is not in the journal with a written plan, it did not
  happen. No revenge or FOMO entries — the program is partly a test of *not* trading.
- **Follow your own rules.** The value is in discovering where you deviate. Deviations are the most
  useful data you will collect.

A word on mindset for the 30 days: the goal is **repeatability**, not a hero month. If you finish
with ten trades that each passed the checklist, were sized correctly, and were managed to plan — even
if the P&L is flat or slightly red — you have *succeeded*, because you have proven a process that will
compound over hundreds of trades. If you finish up money because you doubled size on a hunch that
happened to work, you have *failed the program* while winning the month, and that habit will end you
later. Judge yourself on adherence, not dollars.

### Minimum trade variety (required for graduation)

Across the 30 days you must open and journal **at least**:

- **One income / neutral structure** — an iron condor, iron butterfly, or credit spread (high-IV,
  premium-selling).
- **One directional trade** — a debit or credit vertical, or a single leg with a clear thesis.
- **One time spread** — a calendar, diagonal, or poor man's covered call.
- **At least one deliberate adjustment** — take a tested position and *manage* it per module 09
  (roll, roll the untested side, convert to a fly, or delta-hedge), with **before/after** analyzer
  snapshots in the journal. (The exit gate requires **two** managed positions.)
- Total: **≥ 10 paper trades**, journaled, with **≥ 2 managed/adjusted** positions.

---

## Week-by-week plan

### Week 1 — Foundations of the process (build the habit, not the P&L)

- **Goal:** establish sizing, journaling, and the checklist as automatic. P&L is irrelevant this week.
- **Trades:** open **2–3** positions, at least one **high-IV income structure** (e.g., an iron condor
  sized to 1–2% max loss). Keep them simple and liquid.
- **Daily:** update the journal on each open position — mark-to-model P&L, current greeks, days to
  management point, any checklist triggers.
- **End of week:** run the **weekly review protocol** (below). Confirm every trade has a written plan
  and correct sizing. Fix any process gaps now.

### Week 2 — Add direction and a time spread

- **Goal:** widen the toolbox; keep the process tight.
- **Trades:** add **one directional** trade (debit or credit vertical matching the IV column) and
  **one time spread** (calendar / diagonal / PMCC). You should now have a small, *diversified* book —
  check portfolio greeks (net delta/vega) against your limits.
- **Daily:** journal; watch how positions with different greeks respond to the same market move.
- **End of week:** weekly review. Aggregate portfolio greeks; note any concentration.

### Week 3 — Management under fire

- **Goal:** deliberately practice **adjustments**. This is the heart of the program.
- **Trades:** you will likely have a **tested** position by now — manage it per module 09 (roll for a
  credit, roll the untested side, convert to a fly, or delta-hedge) and record **before/after**
  snapshots (payoff, greeks, POP). If nothing is tested, *construct* a scenario: take an existing
  position, assume an adverse move, and paper-trade the adjustment. Hit the **21-DTE decision** on any
  position reaching it — take winners, roll, or close.
- **Daily:** journal, with special attention to the adjust-vs-close decision (thesis intact?).
- **End of week:** weekly review focused on management quality.

### Week 4 — Consolidate and write the plan

- **Goal:** close out or roll remaining positions cleanly, and **write your trading plan**.
- **Trades:** manage existing positions to their exits; open only what fits and completes your
  required variety. Ensure you have ≥ 10 trades and ≥ 2 managed.
- **Daily:** journal; begin drafting the trading plan using the template below.
- **End of week:** final weekly review **plus** the completed **written trading plan**. That plan +
  the reviewed journal is graduation (exit gate 4).

---

## The daily journal requirement

Every day the market is open and you have an open position, write a short note per position:

```
Date: ______   Underlying: ______   Position #: ______   DTE: ______
- Spot / IV now: ______ / ______
- Mark-to-model P&L $ (pnl_at): ______   |  % of max profit/loss: ______
- Position greeks (Δ/Θ/V): ____ / ____ / ____
- Status vs plan: on track / near profit target / tested / at 21 DTE / event soon
- Action today: none / took profit / adjusted (how) / closed (why)
- One line: what the position is teaching me today.
```

The daily note takes two minutes and is where you catch a tested position before it becomes a max
loss, and a winner before you give it back.

---

## The weekly review protocol

Once a week, sit down (30–45 minutes) and work through this in order:

1. **Every open position vs its plan.** Is each on track? Any at the profit target, loss trigger, 21
   DTE, or with an event approaching? Decide the action per the exit checklist.
2. **Portfolio greeks.** Aggregate net delta / theta / vega across the book. Inside your limits? Any
   accidental concentration (all long delta, all short vega, all one underlying)?
3. **Closed trades since last review.** For each: P&L as **% of max loss** (not raw dollars), and —
   more important — **did I follow my plan?** Tag any deviation with a mistake category (sizing /
   selection / management / psychology).
4. **Mistake patterns.** Look across all trades so far for a recurring leak. One repeated mistake
   corrected is worth more than any new strategy.
5. **Process check.** Did every new trade pass the entry checklist and sizing rule? Any revenge / FOMO
   / overtrading creeping in? Any trade you should *not* have taken?
6. **Adjust the plan (not the rules mid-trade).** If a rule is genuinely wrong, note it to revise in
   the written plan — but never move a stop or target mid-trade to avoid a loss.

---

## The final deliverable: your written trading plan

This is the graduation document. A trading plan is the constitution you trade under — written when
calm, obeyed when not. Fill in every section with **specific, numeric** answers (not "trade good
setups").

```
========================  MY OPTIONS TRADING PLAN  ========================
Version: ___   Date: ___   Account equity (paper/real): ___

1. MISSION & SCOPE
   - Why I trade options (income / directional / vol / learning): ___
   - Time I can commit (screens per day, review cadence): ___
   - What I will NOT do (e.g., no naked calls, no earnings gambles): ___

2. MARKETS & INSTRUMENTS
   - Underlyings I will trade (liquid names/ETFs), and how many at once: ___
   - Liquidity standards (max bid/ask width, min OI/volume): ___
   - Products I will avoid (illiquid, hard-to-borrow, etc.): ___

3. STRATEGIES (my matrix)
   - Neutral / high-IV: ___ (e.g., iron condor, ~16Δ shorts, 30-45 DTE)
   - Neutral / low-IV: ___
   - Bullish / high-IV and low-IV: ___
   - Bearish / high-IV and low-IV: ___
   - Time spreads / long-vol: when and which: ___
   - Structures I am NOT yet allowed to trade: ___

4. ENTRY RULES
   - IV rank thresholds for selling vs buying: ___
   - DTE ranges by strategy: ___
   - Strike selection (delta targets, expected move): ___
   - Event rule (earnings/ex-div avoidance or deliberate): ___
   - Entry checklist must pass in full: Y

5. POSITION SIZING & PORTFOLIO LIMITS
   - % of equity risked per trade (by max loss): ___%
   - Max concurrent positions / max per underlying: ___
   - Portfolio limits: net delta [___, ___], net vega [___, ___], theta target: ___
   - Cash/buying-power buffer kept: ___%

6. MANAGEMENT & ADJUSTMENT RULES
   - Profit target (e.g., 50% of credit / 25% of fly): ___
   - Loss trigger and action: ___
   - 21-DTE decision rule: ___
   - Adjustment playbook (roll for credit, roll untested side, convert to fly,
     delta-hedge) and when each applies: ___
   - Adjust-vs-close test: would I open this today? If no -> close.

7. EXIT RULES
   - How winners are taken: ___
   - How losers are closed: ___
   - Expiration/assignment/pin handling: ___

8. RISK OF RUIN & DRAWDOWN RULES
   - Max account drawdown before I stop and reassess: ___%
   - Rule after a losing streak (same size, same checklist; no upsizing): ___

9. PSYCHOLOGY & PROCESS
   - My known biases and their triggers: ___
   - Rules that neutralize them (written stops, fixed size, trade caps): ___
   - Journaling & weekly-review commitment: ___

10. REVIEW CADENCE
   - Daily: ___   Weekly: ___   Monthly/quarterly plan revision: ___
==========================================================================
```

A good plan is boring, specific, and slightly conservative. If you cannot answer a section with
numbers, that is a gap to close before trading real money.

---

## What paper trading can and cannot teach

Be clear-eyed about the tool. Paper trading **can** teach you the mechanics of order entry, the
rhythm of journaling and review, how a structure's greeks actually behave as price and time move,
whether your sizing math is right, and — most valuably — whether you *follow your own rules*. Those
are the exact skills the capstone is testing, and they transfer directly.

Paper trading **cannot** replicate two things: real **slippage** and real **emotion**. A paper fill
is often the mid; a real fill is worse, and on four-leg structures that gap between paper and real
P&L is significant — which is why you record the mid *or worse*, never the perfect price. And no
simulator makes your stomach drop when a position is down real rent money; the discipline that holds
under paper stress is a floor, not a guarantee, for how you will behave with capital at risk. The
honest way to close that gap is to (a) trade paper as if it were real — no do-overs, no
"I-would-have-closed-that," no untracked trades — and (b) when you do go live, start at a size so
small that a maximum loss is emotionally trivial, and scale only as the journal proves the process
holds. Treat the 30 days as *rehearsal under real staging*, and the transition to real money as a
continuation of the same journal, not a fresh start.

## Common ways learners fail the program

Know the traps in advance so you can avoid them:

- **Trading for volume, not variety.** Twenty near-identical condors is not a portfolio and does not
  satisfy the variety requirement — it is one bet twenty times. Hit the required structure types
  deliberately.
- **Skipping the daily note when nothing is happening.** The quiet days are when you catch a position
  drifting toward its management point *before* it is tested. Two minutes a day.
- **Retro-fitting the plan.** Writing the "plan" for a trade *after* you opened it defeats the entire
  purpose. The plan — target, stop, adjustment, exit — is written before entry or the trade does not
  count.
- **Never letting a loser be a loser.** Some learners adjust everything to avoid ever booking a loss,
  turning small planned losses into large complex ones. A plan-sized loss taken cleanly is a *success*
  of the process, not a failure.
- **Manufacturing zero adjustments.** If the month is calm and nothing gets tested, you still owe the
  gate two managed positions — *construct* the scenario (assume an adverse move on an open position
  and paper-trade the defense with before/after snapshots). Do not skip the module-09 practice.
- **P&L tunnel vision.** Judging the month by dollars made rather than rules followed. Over 10 trades,
  variance dominates; process is the only thing you can actually evaluate this early.

## Graduation (exit gate 4)

You graduate the curriculum when you can show:

1. **The written trading plan** above, every section filled with specific answers.
2. **A journal of ≥ 10 paper trades**, each with a pre-entry plan and a post-exit review.
3. **≥ 2 managed/adjusted positions** with before/after analyzer snapshots (payoff, greeks, POP).
4. **The required variety**: at least one income structure, one directional, and one time spread.
5. **Evidence you followed your own rules** — or an honest accounting, in the journal, of where you
   did not and what you changed.

Meeting these is not a license to size up. The sizing rules from module 10 apply from the first real
dollar, and modules 08–09 should be revisited quarterly because regimes change and so should your
defaults.

---

## Key takeaways

- The capstone deliverable is a **process**, proven by a journal and a written plan — not a P&L number.
- Run the 30 days with **fixed sizing, full journaling, and the checklists** from day one; treat paper
  as if it were real.
- Hit the **required variety** (income + directional + time spread) and, above all, **practice
  adjustments** — two managed positions with before/after snapshots.
- The **weekly review** hunts for *mistake patterns*; one recurring leak fixed beats any new strategy.
- The **written trading plan** is your constitution: specific, numeric, conservative, obeyed when calm
  and when not.
- Graduation is a beginning. Trade small and real only after the gate, keep sizing tiny, journal
  forever, and revisit the regime and adjustment modules every quarter.

## After the curriculum

Build **v2** of `optionslab` from `SPEC.md` (live chains + an IV-rank screener that ranks structures
from your module-08 matrix), then the Streamlit builder (v3) and the backtester (v4). Turning the
rules you just wrote into software that enforces them is the deepest study of all — and the best way
to keep yourself honest.
