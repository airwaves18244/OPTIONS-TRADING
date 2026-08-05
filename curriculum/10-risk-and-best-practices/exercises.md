# 10 — Exercises: Risk and Best Practices

Calculation, judgment, and one "break it." Verify numeric answers with `analyzer.max_loss` and
`greeks.position_greeks`. Use the DEMO chain unless stated.

---

**1. (Calculation) Size it.** Your account is `$30,000`; you risk **2%** per trade. A DEMO iron
condor 87.5/92.5/107.5/112.5 has a max loss of `$360`. How many condors do you trade? Show the
formula and the rounding.

**2. (Calculation) Premium ≠ risk.** A bull put spread collects `$140` credit and is `$5` wide. A
beginner sizes it as "risking `$140`" and on a `$20,000` account at 2% puts on **two** spreads. What
is the spread's actual max loss, how much is truly at risk with two spreads, and what % of the
account is that? What should the correct size have been?

**3. (Calculation) Portfolio greeks.** You hold: (i) the condor above, (ii) a bull put spread 95/90,
(iii) a bull call spread 100/110. Aggregate the net delta and net vega with
`greeks.position_greeks` at spot 100, vol 0.26. Is the book net long or short delta? Net long or
short vega? What single market event is this book most exposed to?

**4. (Scenario) Diversification check.** A trader is proud of holding eight positions. On inspection:
six are iron condors on large-cap tech names, one is a short strangle on a tech ETF, one is a covered
call on another tech name. Is this diversified? What is the *one* market event that could make all
eight lose at once, and what would you change?

**5. (Scenario) Liquidity veto.** Structure A: a four-leg iron condor on an illiquid name, options
`$0.40` wide, open interest ~30 per strike, theoretical credit `$1.60`. Structure B: a two-leg bull
put spread on a liquid ETF, options `$0.03` wide, huge OI, credit `$1.20`. Which do you trade and
why, in terms of realized edge?

**6. (Scenario) Earnings.** You want to sell a 30-DTE iron condor on DEMO for range income. DEMO
reports earnings in 18 days. State two acceptable ways to handle this and one unacceptable one.

**7. (Concept) Assignment around ex-dividend.** You are short a DEMO 95 call that is `$6` ITM, and
DEMO goes ex-dividend tomorrow. What specific risk do you face tonight, why does it happen, and what
do you do?

**8. (Concept) PDT.** Your account holds `$18,000`. Explain the Pattern Day Trader rule and one
concrete way it constrains how you manage short-DTE options positions.

**9. (Break it) Find the flaw.** "I lost `$500` on my last condor. To make it back fast, I'm putting
on the same condor at **triple** size on the same underlying, because I'm now sure it'll revert. It's
still 'only' 6% of my account at risk, and I don't need a written exit plan — I'll know when to get
out." List at least four problems, tagging each with the psychology or risk concept involved.

---

## Answer key

**1.** `units = floor(equity × risk% / |max_loss|) = floor(30,000 × 0.02 / 360) = floor(600 / 360) =
floor(1.67) = **1 condor**`. Always round **down** — 1.67 is not "close enough to 2"; two condors
would risk `$720` = 2.4% of the account, over your limit.

**2.** The spread's max loss = width − credit = `$500 − $140 = $360` per spread. **Two** spreads risk
`$720`, which is `720 / 20,000 = 3.6%` of the account — well over the 2% rule. Correct size:
`floor(20,000 × 0.02 / 360) = floor(400/360) = **1 spread**`. Sizing by the `$140` premium instead of
the `$360` max loss understated the risk by ~2.6× and led to over-sizing.

**3.** Net delta ≈ **+51** (long), net vega ≈ **−8** (short). The two bullish spreads (long delta)
outweigh the condor's small short delta, so the book is **net long delta** despite containing a
"neutral" trade; the short-vol condor dominates vega, so the book is **net short vega**. The event it
is most exposed to: a **sharp sell-off with a volatility spike** — falling prices hurt the net-long
delta *and* rising IV hurts the net-short vega simultaneously. (Values from
`greeks.position_greeks` at spot 100, vol 0.26.)

**4.** **Not diversified** — it is essentially one big bet on large-cap tech staying quiet with low
vol. All eight are (a) the same underlying *sector* (correlated) and (b) the same *strategy posture*
(short premium / short vol). The single event that sinks all eight: a **tech-sector-wide sell-off
with a vol spike** (correlations go to 1, every short-premium position gets tested at once, the short
strangle's undefined risk balloons). Changes: spread across **uncorrelated underlyings/sectors**,
mix in **directional and long-vol** trades, ladder **expirations**, and cap total short-vega exposure.

**5.** **Trade B.** Structure A's `$0.40`-wide markets on four legs mean you cross ~`$0.40` × (four
legs, in and out) — a large fraction of the `$1.60` credit is eaten by slippage on entry *and* exit,
and the thin OI (30) means you may not get filled adjusting or closing. Structure B's `$0.03`-wide,
high-OI ETF options preserve almost all of the `$1.20` credit as realized edge and let you get out
cleanly. **Liquidity is a veto**: a smaller theoretical credit you can actually capture beats a
larger one you cannot.

**6.** Acceptable: (a) **Choose an expiration that does not contain earnings** (e.g., a shorter cycle
that expires before day 18, or structure it to be closed before the report). (b) **Trade the earnings
deliberately with defined risk** (the condor is already defined) sized as if it will go against you,
knowing the post-earnings **vol crush** is the thesis — and accept the gap risk. Unacceptable: **put
on the 30-DTE condor and ignore the earnings**, holding undefined-of-gap exposure through a binary
event by accident — an after-hours gap through a short strike can be a max loss no adjustment
prevents.

**7.** Risk: **early assignment tonight.** A short ITM call is likely to be exercised by its holder
the day **before** ex-dividend to capture the dividend; you would be **assigned, ending up short 100
shares** and **owing the dividend**, with unexpected directional exposure and margin use overnight.
It happens because exercising captures a dividend that exceeds the call's remaining extrinsic value.
What to do: **close (or roll) the short ITM call before the ex-dividend date** rather than carry the
assignment risk.

**8.** The **Pattern Day Trader** rule: a US margin account **under `$25,000`** that makes **4 or more
day trades within 5 business days** is flagged PDT and restricted from further day trading until it is
funded above `$25k`. With `$18,000` you are subject to it. Concrete constraint: you cannot freely
**open and close the same short-DTE position on the same day** repeatedly — if a 0–2 DTE position
needs same-day entry/exit management, those round trips count as day trades and can exhaust your
allowance, so you must plan cadence (hold overnight, use longer DTE, or limit same-day round trips).

**9.** Flaws: (a) **Revenge trading / "make it back fast"** — the entire premise is emotional, not a
fresh checklist-passing setup. (b) **Upsizing to 3× after a loss** breaks the fixed-sizing rule; "only
6%" is still **3× your 2% limit** on a *single* trade, and concentrated in **one underlying** (no
diversification). (c) **"I'm now sure it'll revert"** is **confirmation bias / overconfidence** — the
prior loss is evidence the thesis may be wrong, not more right. (d) **"I don't need a written exit
plan — I'll know"** guarantees **loss-aversion-driven** mismanagement (holding the loser hoping);
rules must be written *before* entry. Correct action: after a loss, the next trade passes the **same
checklist at the same size**, ideally on a **different, uncorrelated** underlying, with a written exit
plan — or take no trade at all.
