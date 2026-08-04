# 11 — Exercises: Capstone

These reinforce the program mechanics and prepare the graduation deliverables. Some are written
(plan/journal) rather than numeric; do them for real — they are the point. Verify any numbers with
`optionslab`.

---

**1. (Setup) Define your program.** Write your program parameters: paper account equity, % risked per
trade, max concurrent positions, max positions per underlying, and portfolio net-delta / net-vega
limits. These become sections 5 of your trading plan. (No single answer — but they must be specific
numbers.)

**2. (Calculation) Week-1 sizing.** On a `$25,000` paper account at 2% risk, you plan to open the
week-1 book from the notebook: iron condor (max loss `$360`), bull call spread (max loss `$318`),
calendar (compute its max loss with `analyzer.max_loss`). How many units of each do you open, and
what is the total capital at risk if all three hit max loss? Is that within a sane portfolio risk
budget?

**3. (Concept) Variety requirement.** List the minimum trade variety required for graduation and map
each to a specific structure you would actually trade, with its target IV environment. Which one are
you least comfortable with, and what will you do about that before day 1?

**4. (Scenario) Week-3 adjustment.** By week 3, your iron condor's put side is tested (spot fell to
93, 25 DTE). Walk through the adjust-vs-close decision and name the specific module-09 adjustment you
would apply, the before/after snapshots you would record in the journal, and the one condition under
which you would close instead of adjust.

**4b. (Judgment) The 21-DTE gate.** Two of your positions reach 21 DTE the same week: position A is a
condor up 55% with both shorts untested; position B is a debit call spread down 30% with the thesis
still intact but slow. State your action on each and why they differ.

**5. (Break it) Critique this "plan."** A peer's entire trading plan reads: *"Trade options on stocks
I like when they look cheap. Sell premium when I can. Cut losers and let winners run. Risk what feels
right. Review when I remember."* Identify at least five things missing or wrong versus the template,
and rewrite two of the sections with specific, numeric rules.

**6. (Review) Run a weekly review.** Take the notebook's week-1 book, imagine it is Friday of week 1,
and run the six-step weekly-review protocol on it in writing: open positions vs plan, portfolio
greeks vs limits, closed trades, mistake patterns, process check, plan adjustments. Produce the
written output you would file.

**7. (Deliverable) Draft the plan.** Fill in **all ten sections** of the trading-plan template from
the lesson with your own specific answers. This is exit gate 4's core artifact — do it completely,
not partially.

---

## Answer key

**1.** Model answer (yours will differ but must be this specific): equity `$25,000`; **2%** (`$500`)
risked per trade by max loss; **max 5 concurrent** positions; **max 2 per underlying**; portfolio net
delta in **[−250, +250]**, net vega in **[−60, +60]**; keep a **30% cash/buying-power buffer**. The
test of a good answer is that every field is a number you could enforce mechanically.

**2.** Condor: `floor(25,000 × 0.02 / 360) = floor(1.39) = **1**`. Bull call spread:
`floor(500 / 318) = floor(1.57) = **1**`. Calendar max loss ≈ the net debit paid (`$125`), so
`floor(500 / 125) = **4**` by the formula — but a calendar's real risk is a fast directional move
losing the whole debit, and you would not put on 4 calendars in week 1; **cap it at 1–2** for
learning and diversification. Total at risk with 1 of each ≈ `360 + 318 + 125 = **$803**` ≈ **3.2%**
of the account across three *diversified-by-strategy* trades — reasonable for a learning book (well
under, say, a 6–8% total-heat ceiling). Note the lesson: the sizing formula is a *maximum*, not a
mandate to fill it.

**3.** Required: (a) **income/neutral** → e.g., iron condor, ~16Δ shorts, 30–45 DTE, **high IV rank**;
(b) **directional** → e.g., bull call debit spread in **low IV** or bull put credit spread in **high
IV**; (c) **time spread** → e.g., a calendar at the pin (front IV rich) or a PMCC, **moderate/rising
vol**; (d) **≥ 1 deliberate adjustment** (two for the gate). The "least comfortable" answer is
personal — the required action is to **paper-trade that structure first in the notebook** (build it,
`summarize` it, stress it with `scenario_grid`) until the risk is intuitive, before risking it in the
program.

**4.** Adjust-vs-close: **is the thesis intact?** If the drop to 93 is noise and you still expect the
range to hold, **adjust**; if it broke on real news (thesis dead), **close**. Assuming intact, the
module-09 move is to **roll the untested call side down for a credit** (banks credit, lowers the
tested-side breakeven, cuts max loss) and/or roll the tested put side out-and-away for a credit.
Journal snapshots: **before** (payoff curve, `position_greeks`, POP, breakevens) and **after** the
adjustment, plus the roll's net credit. Close instead of adjust when: no credit roll is available
(would be a debit), the thesis is broken, or defending would push the position past your risk limits.

**4b.** Position A (condor, +55%, untested, 21 DTE): **take the winner off** — short gamma turns
violent in the last three weeks and there is little premium left to justify the risk; redeploy into a
fresh cycle. Position B (debit call spread, −30%, thesis intact, slow): a **long** debit spread has
*positive*, benign gamma near expiry and defined risk, so the 21-DTE gamma urgency does not apply the
same way — you may **hold or roll out** if you still believe the move. They differ because the
**short-gamma** position is the one the 21-DTE rule is really about.

**5.** Missing/wrong vs the template: (1) **no numeric sizing rule** ("risk what feels right" — the
cardinal sin); (2) **no IV-rank thresholds** ("when they look cheap" / "when I can" is not a rule);
(3) **no specific strategies mapped to the matrix**; (4) **no management/adjustment rules or 21-DTE
decision**; (5) **no portfolio limits or diversification rule**; (6) **no defined review cadence**
("when I remember"); (7) **no drawdown / losing-streak rule**. Rewrite examples — *Sizing:* "Risk 2%
of equity per trade by `analyzer.max_loss`, max 5 concurrent, max 2 per underlying." *Entry:* "Sell
premium only when IV rank ≥ 50; buy premium/debit when IV rank ≤ 30; 30–45 DTE for income; no
earnings inside the horizon."

**6.** A complete answer files written notes for all six steps. Example skeleton: **(1) Positions vs
plan:** condor on track (mid-range, 38 DTE), bull call spread slightly green (thesis intact),
calendar near pin — none at profit target or 21 DTE yet. **(2) Greeks:** net delta ~ +X (long, from
the call spread), net vega ~ −Y — within limits; note the book leans long/short-vol. **(3) Closed:**
none yet. **(4) Patterns:** none (week 1) — but confirm all three passed the checklist. **(5)
Process:** all sized to ≤2%, all journaled, no revenge/FOMO entries. **(6) Plan adjustments:** none
mid-trade; note any rule ambiguity to revise later. The grade is on *completeness and honesty*, not
P&L.

**7.** No key — this is your deliverable. A passing plan has **every one of the ten sections filled
with specific, numeric, enforceable answers**, consistent with your exercises above. If any section
is vague ("trade good setups", "size appropriately"), it is not done. Bring the completed plan plus a
journal of ≥ 10 paper trades (≥ 2 managed, with before/after snapshots) to graduate — exit gate 4.
