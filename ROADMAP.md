# ROADMAP — The Options Learning Workflow

This is the workflow. Follow it in order. Each module lives in `curriculum/<module>/` and contains:

- **`lesson.md`** — the theory: mechanics, when to use, management rules, best practices.
- **`notebook.ipynb`** — the lab: build it, price it, plot it, stress it with `optionslab`.
- **`exercises.md`** — problems and scenario drills, with an answer key at the bottom.

**Rules of the road**

1. Never skip a module's exit gate. Speed is not the goal; skipping gates is how accounts blow up.
2. Every strategy lesson uses the same template — learn to think in it:
   *mechanics → payoff & greeks profile → market condition + IV environment it fits → entry
   criteria → management/adjustment rules → exit rules → common mistakes*.
3. From Phase 2 onward you paper-trade in parallel. One or two positions at a time, journaled.
4. The notebook is not optional. Change the numbers, break the strategy, watch what the greeks do.

---

## Weekly cadence (per module)

| Day | Activity |
|---|---|
| 1–2 | Read `lesson.md`. Take notes in your own words. |
| 3 | Work through `notebook.ipynb`; then change strikes, vol, and days-to-expiry and re-run. |
| 4 | Do `exercises.md` without looking at the key; check afterwards. |
| 5 | (Phase 2+) Open or manage a paper trade applying the module. Journal it. |
| 6–7 | Review journal + notes. Attempt the exit gate. Pass → next module. Fail → repeat days 3–4. |

Expect roughly **one module per week** (12–16 weeks total). Faster is fine if gates pass honestly.

---

## Phase 1 — Foundations (modules 00–02)

> Goal: read an option chain fluently and explain any option's price through its greeks and IV.

### `00-foundations` — Options mechanics refresher
Calls and puts from the contract up: moneyness (ITM/ATM/OTM), intrinsic vs extrinsic value,
expiration cycles and DTE, exercise & assignment (and why early assignment happens), settlement,
the option chain, bid/ask and liquidity, multiplier and notional, order types. Pricing intuition:
what makes premium move. Lab: price options with `optionslab.pricing`, decompose premium into
intrinsic + extrinsic across strikes.

### `01-greeks` — The greeks
Delta (directional exposure *and* rough ITM probability), gamma (delta's speed; why it explodes
near expiry), theta (decay; who pays it, who earns it), vega (vol exposure), rho (brief).
Position-level greeks: summing across legs, what a "delta-neutral, short-vega" book means.
Lab: greeks curves vs spot and vs time with `optionslab.greeks` + `viz.plot_greeks`.

### `02-volatility` — Volatility, the option trader's raw material
Historical vs implied vol; IV as the market's price of uncertainty; IV rank / IV percentile and
why "high or low IV" only means something relative to the underlying's own history; skew and why
puts trade rich; term structure; earnings and event vol (the crush). The single most important
strategy-selection input: **is IV high or low right now?**
Lab: compute HV from price series, back out IV from sample chains, plot skew and term structure.

**Exit gate 1:** Take an unfamiliar option chain from `data/samples/` and, for three different
strikes, explain the premium: intrinsic/extrinsic split, what each greek says the position will
do, and whether IV is rich or cheap versus HV — without running code first, then verify in the
notebook.

---

## Phase 2 — Core strategies (modules 03–05)

> Goal: for every strategy here, state from memory the market view + IV condition it expresses,
> its max risk, and its management rule — *before* opening it.

### `03-single-leg-and-stock` — Single legs and stock combos
Long call, long put (directional debit trades; theta works against you). Covered call,
cash-secured put (the income workhorses; assignment as a feature). Protective put, collar.
When each fits: direction, conviction, IV level. Why buying options in high IV and selling them
in low IV are both uphill battles.

### `04-vertical-spreads` — Defined-risk directionality
Bull call / bear put (debit verticals), bull put / bear call (credit verticals). Strike selection,
risk/reward vs probability trade-off, debit-vs-credit choice as an IV decision, spread width and
sizing. Managing winners early (the "take it at 50%" rule for credit spreads) and losers at the
short strike.

### `05-neutral-income` — Trading a range, selling volatility
Long/short straddle and strangle (pure vol trades), iron condor (the flagship range trade),
iron butterfly, long butterfly. Wing width, delta-based strike selection (e.g., ~16Δ shorts),
credit targets, expected move vs breakevens. Why these are high-IV strategies, and what gamma
risk near expiry does to them.

**Exit gate 2:** Blind table drill — for each of the 14 strategies in Phase 2: market view,
IV environment, max profit, max loss, breakevens formula, primary management rule. Then verify
your table against `optionslab.analyzer.summarize` for a concrete example of each.

---

## Phase 3 — Complex structures & regime selection (modules 06–08)

> Goal: given a market scenario (direction + IV + horizon), pick a structure and justify it.

### `06-time-spreads` — Trading the calendar
Calendar spreads (short front vol/theta, long back), diagonals, the poor man's covered call
(PMCC). Term-structure logic, earnings calendars, why mixed expiries need the analyzer's
mark-to-model P&L (`pnl_at`) instead of a simple expiry payoff.

### `07-advanced-structures` — Asymmetric and ratio structures
Call/put ratio spreads, backspreads (long gamma for cheap, tail-risk trades), broken-wing
butterfly (income with no risk on one side), jade lizard (no upside risk short premium).
When the extra complexity is actually paid for — and when it isn't.

### `08-market-conditions` — The strategy selection matrix
The module that ties everything together. A decision framework:
**direction (bullish / bearish / neutral) × IV level (high / low) × horizon** → candidate
structures, with tie-breakers (liquidity, account size, event risk, assignment tolerance).
Regime awareness: trending vs ranging markets, vol regimes, event calendars.
Lab: scenario drills — the notebook deals you market setups; you pick and build the structure,
then the analyzer scores your choice against alternatives.

**Exit gate 3:** Ten written scenario drills from module 08's exercise set: pick a structure,
justify it in the matrix's terms, state entry criteria and the exit/adjustment plan. Compare
against the answer key's reasoning (structures may differ; reasoning must hold).

---

## Phase 4 — Management & mastery (modules 09–11)

> Goal: a written trading plan, and demonstrated ability to manage a position when the market
> moves against it.

### `09-adjustments` — Tuning open positions when the market changes
The module you asked for by name. The adjust-vs-close decision framework (adjust only when the
original thesis still holds). Rolling: out (time), up/down (strikes), out-and-away (both); rolling
for a credit as the iron rule. Defending tested credit spreads and iron condors (rolling the
untested side, going inverted, converting to a fly). Delta hedging with stock or options.
The ~21-DTE decision point and gamma-risk avoidance. Repair strategies for broken long stock/calls.
Lab: the analyzer's scenario grid (`analyzer.scenario_grid`) replays adverse moves against your
open positions; you apply each adjustment and compare resulting P&L surfaces and greeks — this is
the tool's reason to exist.

### `10-risk-and-best-practices` — The professional wrapper
Position sizing (risk a fixed small % per trade; size by max loss, not premium), portfolio-level
greek limits, diversification across underlyings/expiries/strategy types, liquidity standards
(spreads, open interest), avoiding earnings surprises (unless trading them deliberately),
the trade journal (template included), entry/exit checklists (included), psychology: loss
aversion, revenge trading, overtrading, FOMO. Broker mechanics: margin, assignment risk around
ex-dividend, PDT considerations.

### `11-capstone` — 30-day paper-trading program
A structured program: week-by-week goals, minimum trade variety (one income structure, one
directional, one time spread; at least one deliberate adjustment), daily journal, weekly review
against checklists, and a final written **trading plan** (markets, strategies, sizing rules,
management rules, review cadence). Graduation = the plan plus a reviewed journal.

**Exit gate 4:** The written trading plan, plus a journal showing ≥10 paper trades including at
least 2 managed/adjusted positions with before/after analyzer snapshots.

---

## How the tool grows with you

| While you're in… | The tool part you're using/learning |
|---|---|
| Phase 1 | `pricing`, `greeks`, `viz` — price and plot single options |
| Phase 2 | `position`, `strategies`, `payoff`, `analyzer.summarize` — build & summarize structures |
| Phase 3 | `analyzer` scenario grids, `data` sample chains — compare structures across regimes |
| Phase 4 | Full analyzer workflow as your pre-trade and adjustment checklist |
| After | v2–v4 of `SPEC.md`: live chains & IV-rank screener, Streamlit builder UI, backtester — you build these as projects, which is the deepest learning of all |

---

## After the curriculum

1. Trade small and real only after the capstone gate, if at all — sizing rules from module 10 apply from dollar one.
2. Build v2 (live data + screener) from `SPEC.md` — your first real software project on top of the library.
3. Revisit modules 08–09 quarterly; regimes change, and so should your defaults.
