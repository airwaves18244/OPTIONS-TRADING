# 09 — Exercises: Adjustments

Mix of framework judgment and **before/after numeric** problems. Use DEMO (spot moves stated per
problem). Verify numbers in the notebook with `pricing.bsm_price`, `analyzer`, and
`greeks.position_greeks`. Model prices below use flat vol as stated.

---

**1. (Framework) Adjust or close?** For each, state adjust / close / do-nothing and one sentence why:
(a) You sold a bull put spread because a stock was in an uptrend; it broke below major support on an
earnings miss and is now testing your short strike. (b) You sold a 30-DTE iron condor for range
income; the stock is quiet, mid-range, 28 DTE, both shorts ~15Δ. (c) You bought a call debit spread,
still bullish, thesis intact, but the stock stalled and you are at 22 DTE with the position slightly
red.

**2. (Concept) The roll-for-credit rule.** Why is rolling a losing position for a *net debit* usually
a mistake, and what is the one legitimate exception named in the lesson?

**3. (Before/after — short put roll).** You are short the DEMO 95 put, 45 DTE, entered for 1.58.
DEMO falls to 92; 20 days pass (25 DTE left); IV rises to 0.32. (a) Compute the model buyback price
of the 95 put and the realized P&L of closing it. (b) You roll **down-and-out** to the 90 put at 120
DTE; compute the new put's model price and the net roll cash — is it a credit? (c) Report the new
position's POP and delta at spot 92 and compare to the un-rolled position's. Did the adjustment
improve the forward position?

**4. (Before/after — condor, roll untested side).** DEMO iron condor 87.5/92.5/107.5/112.5, now 25
DTE, IV 0.30, DEMO at 93 (put side tested). You roll the untested call spread **down** from
107.5/112.5 to 102.5/107.5. Using model prices: (a) what net credit does the roll add? (b) What
happens to the campaign credit, the **downside** breakeven, and max loss? (c) What did you give up?

**5. (Before/after — convert to fly).** Same condor, DEMO now **breached** to 92 with 20 DTE, IV
0.31. You convert the short put spread (long 87.5 / short 92.5) into a long put butterfly by selling
one more 92.5 put and buying a 97.5 put. (a) What is the net debit to add the legs? (b) Compare max
loss and max profit of the breached spread vs the converted fly. (c) Why is paying a debit acceptable
here when the roll-for-credit rule says otherwise?

**6. (Calculation — delta hedge).** The short 95 put at spot 92 (25 DTE, IV 0.32) carries about +63
dollar-deltas. You want the position delta-flat because your view is still range-bound. (a) How many
shares, long or short, neutralize it? (b) After hedging, what is the position delta, and what new
risk did the hedge introduce?

**7. (Scenario) The 21-DTE decision.** You hold a 45-DTE iron condor now at 21 DTE, up ~55% of max
profit, both shorts untested. State the three choices the lesson gives at this decision point and
which you would take here, with one sentence of gamma-risk reasoning.

**8. (Break it) Find the flaw.** "My short call spread went against me — the stock ripped through my
short strike. I'm not worried, my thesis is that it reverts. I'll roll the spread *up and out* to
next month, and since that roll costs a small debit I'll just pay it; I'll also sell a naked put to
bring in extra premium to fund the roll." List at least three problems.

---

## Answer key

**1.** (a) **Close.** The thesis (uptrend, support holding) is *broken* by the earnings miss and
support break — you would not open this bull put spread fresh today, so do not "defend" it. (b)
**Do nothing.** Quiet, mid-range, shorts still ~15Δ, well before the 21-DTE point — theta is working;
no trade needed. (c) **Adjust (or hold).** Thesis intact, so rolling the debit spread out for more
time is reasonable if it stalls; at 22 DTE you are near the decision point but a debit spread's gamma
risk is far lower than a short-premium position's.

**2.** Rolling for a debit means you are **paying cash to increase or prolong risk** on a position the
market is now pricing against you — usually a signal the thesis is broken and you should close, not
add. It also *raises* your max loss. The one legitimate exception: paying a **small, deliberate debit
to convert undefined risk into defined risk** (e.g., buying a wing, or converting a breached spread to
a butterfly) — that is buying insurance/a cap, not doubling down.

**3.** (a) Model buyback of the 95 put at spot 92, 25 DTE, vol 0.32 ≈ **4.85**; realized P&L of
closing = (4.85 − 1.58) × (−1) × 100 ≈ **−\\$327** (you sold at 1.58, buy back at 4.85). (b) New 90
put at 120 DTE ≈ **5.70**; net roll cash = (5.70 − 4.85) × 100 ≈ **+\\$85 → a credit**. (c) New
position POP@92 ≈ **0.66** vs un-rolled ≈ **0.41**; delta ≈ **+41** vs **+63**. Yes — lower obligation
strike (95 → 90), more time, higher forward POP, flatter delta, and a fresh credit. The −\\$327 is
sunk; the forward trade is materially better.

**4.** (a) Roll net ≈ **+\\$22 credit** (new 102.5/107.5 spread credit minus the cost to close the old
107.5/112.5 spread, both at model). (b) Campaign credit rises **\\$140 → \\$162**; the downside
breakeven improves **91.10 → 90.88** (more room on the tested put side); max loss shrinks **−\\$360 →
−\\$338**. (c) You gave up **upside room**: the upper breakeven drops **108.9 → 104.1** and POP dips
slightly (~0.57 → ~0.53) because the profit band narrowed on top. Net: you harvested the safe side's
profit to defend the tested side.

**5.** (a) Add legs at spot 92, 20 DTE, vol 0.31: sell 92.5 put ≈ 2.93, buy 97.5 put ≈ 6.33 → net
debit ≈ **\\$340**. (b) Breached put spread: max loss ≈ **−\\$436**, max profit ≈ **+\\$64**.
Converted fly (87.5/92.5/97.5): max loss ≈ **−\\$276**, max profit ≈ **+\\$221** (at the 92.5 body).
(c) Rolling for a credit is unavailable on a genuinely breached side, and the debit here **buys a cap
on the loss** (−\\$436 → −\\$276) *and* a recovery tent — it is insurance, the named exception, not
doubling down. Your probability of profit falls (the fly wins only in a narrow band), which is the
honest cost of capping.

**6.** (a) Each share is 1 delta, so **short ~63 shares** offsets the +63 deltas. (b) Position delta
≈ **0** (flat). New risk introduced: the hedge is itself a **directional (short-stock) position** —
if DEMO reverses up, the short shares lose while the put recovers; you have converted directional
risk into path/whipsaw risk and now must manage the hedge (re-hedge to a band, cover it if your view
turns directional). Shorting stock also uses buying power and requires borrow.

**7.** The three choices: **(i) take the winner off** (close near the profit target and redeploy into
a fresh ~45-DTE cycle), **(ii) roll the whole position out** to the next cycle for a credit (buys time
and *reduces* gamma), or **(iii) close a loser** whose thesis broke. Here, up ~55% and untested,
**take it off** — a condor's short gamma turns violent in the last three weeks, and there is little
premium left to justify carrying that risk.

**8.** Flaws: (a) **Rolling for a debit** violates the credit rule — you are paying to prolong a
losing trade; if you cannot roll for a credit, that is the market telling you to close. (b) **Selling
a naked put to "fund" the roll adds a whole new undefined-risk position** in the *opposite* direction
— you would be short a call spread *and* short a put, i.e., a strangle, doubling your exposure and
your margin right when you are already wrong. (c) The reasoning is **"my thesis is it reverts,"** but
the stock ripping *through* the short strike is evidence the thesis is broken — "it'll come back" is
hope, not analysis. (d) No mention of **defined-risk alternatives** (convert the breached call spread
to a fly to cap the loss) or of simply **closing** for a defined loss. Better plan: if the thesis is
truly intact and a credit roll exists, roll up-and-out for a credit; if not, cap it with a fly or
close — never fund a defense by selling naked premium on the other side.
