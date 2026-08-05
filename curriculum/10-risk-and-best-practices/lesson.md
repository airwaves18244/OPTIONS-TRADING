# 10 — Risk and Best Practices: The Professional Wrapper

You can now build almost any structure, choose it for the regime, and defend it when it goes wrong.
None of that matters if you size trades so large that one bad month ends you, or if you abandon the
process the moment fear or greed shows up. This module is the wrapper that keeps the rest alive: how
much to risk per trade, how to keep the whole book from becoming one giant correlated bet, which
trades to refuse on liquidity or event grounds, and — the part nobody wants to hear — how to manage
the person pressing the buttons. It is deliberately unglamorous. The edge in options is not a secret
structure; it is surviving long enough, with enough capital intact, for a repeatable process to
compound. This lesson gives you the sizing math, the portfolio limits, the checklists, the journal,
and an honest look at the psychology that decides whether you follow any of it.

---

## Position sizing: the one rule that keeps you solvent

Everything starts here, because sizing is the only variable that is fully in your control and the
only one that can end you regardless of how good your strategy is.

### Risk a small fixed percentage of the account per trade

The professional standard for a single defined-risk options position is to risk **1–2% of account
equity** on any one trade, and rarely more than **5%** even with high conviction. "Risk" means the
dollars you can actually lose — the position's **max loss**, not the premium or the buying power.

The formula is simple:

> **Max contracts (or spreads) = (account equity × risk %) ÷ (max loss per unit)**

On a `$25,000` account risking 2% (`$500`) with a spread whose max loss is `$360`, you trade **one**
spread (`$500 ÷ $360 = 1.38`, round *down*). The tool gives you the denominator directly:
`analyzer.max_loss(position)` returns the max loss as a negative dollar number; take its absolute
value and divide. Always round **down** — never up into "close enough."

### Size by max loss, not by premium

A credit spread that collects `$140` is not a `$140` risk; if it is `$5` wide, its max loss is
`$360`. A cash-secured put's real risk runs toward the strike (a `$95` put is a `~$9,500` obligation,
minus credit). Naked/undefined structures have max loss `-inf` — you cannot size them by a formula, so
you size them by a **defined stress scenario** (e.g., "what do I lose if the stock gaps 2× the
expected move?") and treat that as the max loss, or simply do not trade them until the account and
temperament support it. The habit to build: **before every trade, read `max_loss`, and size to your
percentage.** This single discipline outperforms almost every strategy tweak.

### A note on buying-power efficiency vs risk

Brokers quote *buying-power reduction* (margin held), which is not the same as max loss. You can be
"only using 20% of buying power" and still be over-risked if those positions are correlated and each
one's max loss is large. Size by risk first; let buying power be a secondary constraint.

---

## Portfolio-level greek limits

A book of individually-sized trades can still be a disaster if they all lean the same way. Aggregate
your greeks (the tool sums them: `greeks.position_greeks` per position, added together) and set
limits *before* they are breached:

- **Net delta.** Your directional exposure across the whole book, in share-equivalents. Decide a band
  (e.g., "net delta between −200 and +200 per `$25k`") that reflects a *deliberate* market lean, not
  an accidental one. If every position drifted long, you are secretly running a leveraged long-stock
  book — hedge it down (module 09) or close something.
- **Net theta.** Positive theta (you collect decay) is the premium-seller's engine, but too much means
  too much short-gamma risk. Know your daily theta and what it implies about your short-vol exposure.
- **Net vega.** Your exposure to a vol move. A book that is net short vega (lots of condors/credit
  spreads) gets hurt when IV explodes — often exactly when markets fall and your deltas hurt too.
  Cap net vega so a single vol spike cannot take out the account. Consider a long-vega position (a
  calendar, a long option) as ballast when you are heavily short vol.
- **Net gamma.** Usually the mirror of theta for sellers (short gamma). The danger metric near
  expiry — track it and respect the 21-DTE rule that keeps it from exploding.

The point of limits is that they are set when you are calm and enforced when you are not. Write them
into your plan (module 11) as hard numbers.

---

## Diversification

Options traders concentrate risk in ways stock investors do not, because a single earnings event or
vol spike hits every position on that underlying at once. Diversify across:

- **Underlyings.** Do not run five condors on five tech names that move together — that is one bet.
  Spread across low-correlation sectors/products.
- **Expirations.** Laddering expiries avoids having your whole book expire (and hit peak gamma) in the
  same week.
- **Strategy types and direction.** A mix of premium-selling and directional/long-vol trades means no
  single regime shift wipes the whole book. If everything you own profits only from "quiet and IV
  falls," a vol spike is a portfolio-level max-loss event.
- **Time (entry).** Legging into the book over days/weeks rather than deploying all capital at one
  IV/price snapshot.

Diversification is not owning *more* trades; it is owning trades that do not all lose on the same day.

---

## Liquidity standards (a hard filter)

An edge on paper vanishes crossing wide markets. Refuse trades that fail basic liquidity:

- **Tight bid/ask.** Aim for option markets a few cents wide (or a small % of the option price), not
  `$0.50`+ wide. You pay half the spread on entry and half on exit — on four-leg structures that is
  four spreads each way.
- **Open interest & volume.** Prefer strikes with real open interest (thousands) and daily volume, so
  you can get filled and, crucially, *get out* when adjusting.
- **Underlying liquidity.** Trade options on liquid underlyings (large, actively traded names/ETFs).
  Thin underlyings have thin, gappy option chains.
- **Penny vs nickel increments.** Names in penny-increment pilot programs fill better. Wider strike
  spacing (like the 2.5-wide DEMO grid) means fewer precise choices.

Liquidity is a *veto*: the theoretically best structure in an illiquid name loses to a simpler one in
a liquid name.

---

## Earnings and events

Earnings (and other binary events — FDA, major macro prints) are where IV inflates and stocks gap.
Two disciplined stances:

1. **Avoid by default.** For most premium-selling and directional trades, choose an expiration that
   does **not** contain an earnings report, or close before it. A gap through your short strike on
   earnings can turn a managed position into a max loss overnight, and no adjustment saves you from an
   after-hours gap.
2. **Trade it deliberately, defined-risk only.** If you *are* trading the event (selling the IV crush
   with an iron condor/butterfly, or buying convexity you think is under-priced), do it with
   **defined risk**, sized as if it will go against you, knowing the post-event vol crush is the
   whole thesis. Never hold *undefined* risk through earnings by accident.

Keep an event calendar for every underlying (earnings, ex-dividend, product/regulatory dates). The
ex-dividend date matters mechanically: short ITM calls face **early-assignment risk** the day before
ex-dividend (module's broker section below).

---

## The trade journal

You cannot improve a process you do not record. The journal is where edge is found — not in the wins,
but in the patterns across many trades. Log **every** trade at entry and at exit. Copy this template.

```
### Trade #____    Date opened: __________    Underlying: ______   Spot at entry: ______

STRATEGY & THESIS
- Structure: ______________________ (e.g., iron condor 87.5/92.5/107.5/112.5)
- Legs / expiry (DTE): ____________________________________________
- Market view (direction): bullish / bearish / neutral / long-vol
- IV context: IV rank ____   HV ____   IV rich/cheap? __________
- Regime: trending / ranging ; event inside horizon? Y/N: __________
- Why this structure (matrix cell): _______________________________

RISK & SIZING
- Net debit/credit: ______   Max profit: ______   Max loss: ______
- Breakevens: ______   POP at entry: ______   Expected move: ______
- Account equity: ______   % of equity at risk (max loss): ______%
- Entry greeks (Δ/Θ/V): ____ / ____ / ____   Portfolio Δ/Θ/V after: ____/____/____

PLAN (written BEFORE entry)
- Profit target: ______   Loss/stop trigger: ______
- Management point: 21 DTE / 50% / other: __________
- Adjustment plan if tested: ______________________________________
- Exit rule: ______________________________________________________

OUTCOME
- Date closed: ______   Spot at exit: ______   Days held: ______
- Adjustments made (with before/after): ___________________________
- P&L $: ______   P&L % of max loss: ______   vs plan? __________

REVIEW
- Did I follow my plan? Y/N — where did I deviate? ________________
- What did the market/greeks do that I didn't expect? ____________
- Mistake category (if any): sizing / selection / management / psychology / none
- One lesson for next time: _______________________________________
```

Review the journal **weekly** (module 11's protocol). Look for recurring mistake categories — that is
where your real edge, or your real leak, lives.

---

## Checklists

### Pre-trade (entry) checklist — every box before you send

1. **Thesis in one sentence.** Direction + IV + horizon. If you can't state it, don't trade it.
2. **Matrix fit.** Does the structure match the direction × IV × horizon cell? Am I on the correct
   side of the IV column (buyer in low IV, seller in high)?
3. **IV rank checked.** Actually looked at it, not assumed.
4. **Liquidity passed.** Tight markets, real OI/volume, on a liquid underlying.
5. **Events cleared.** No earnings/ex-div inside the horizon — or I am trading it deliberately,
   defined-risk.
6. **Max loss read** (`analyzer.max_loss`) and **sized to ≤ my risk %** (round down).
7. **Portfolio greeks after this trade** stay inside my delta/vega limits.
8. **Written plan exists:** profit target, loss trigger, management point (21 DTE / 50%), adjustment
   plan, exit rule — *in the journal, before entry.*
9. **Not revenge/FOMO.** This trade would look the same if my last trade had won.

### Exit / management checklist — review open positions on a schedule

1. **Profit target hit?** (e.g., 50% of credit) → take it; don't get greedy.
2. **Loss trigger hit?** → act per plan (adjust for a credit if thesis intact, else close).
3. **Tested?** → is the thesis still intact? adjust vs close (module 09). Roll for a credit only.
4. **21 DTE reached?** → decide: take winner / roll out / close loser. Stop feeding short gamma.
5. **Event approaching?** → close or define risk before it.
6. **Portfolio greeks drifted** outside limits? → hedge or trim.
7. **Journal updated** with what you did and why.

---

## Psychology: managing the trader

The framework fails at the exact moments it matters most, because a human is executing it. Name the
enemies so you can catch them:

- **Loss aversion.** We feel losses about twice as intensely as equal gains, which makes us hold
  losers too long ("it'll come back") and cut winners too early. The antidote is *mechanical rules
  written in advance*: a pre-defined profit target and loss trigger remove the in-the-moment feeling
  from the decision.
- **Revenge trading.** After a loss, the urge to "make it back" with a bigger, faster, lower-quality
  trade. This is how a bad trade becomes a bad week. Rule: after a losing trade, the next trade must
  pass the *same* checklist at the *same* size — no upsizing to recover.
- **Overtrading.** Boredom and the feeling that you must always have a position on. Every trade costs
  spread and commission and adds risk; doing nothing is a position. Cap the number of new trades per
  week; require every one to earn its place on the checklist.
- **FOMO.** Chasing a move already made, entering late at a worse price and worse IV. If you missed
  it, you missed it — there is always another setup. The market is not a train you must catch.
- **Confirmation bias & anchoring.** Seeing only evidence that supports your open position, and
  anchoring to your entry price ("I'll exit at break-even") instead of the current thesis. The exit
  test is always *forward*: would I open this today?

The structural defenses are the same three things: **written rules, a journal that makes deviations
visible, and fixed sizing** so no single emotional decision can be catastrophic. Discipline is not
willpower; it is systems that make the disciplined action the default.

---

## Broker mechanics you must know

- **Margin and buying power.** Defined-risk spreads reduce buying power by roughly their max loss.
  Undefined-risk trades (naked options, short strangles) use *margin formulas* (a % of the underlying
  notional, adjusted for moneyness) that can spike as the position moves against you — a **margin
  call** forces liquidation at the worst time. Know each position's buying-power effect and keep a
  cash buffer.
- **Assignment and early exercise.** American equity options can be assigned any time you are short
  and the option is ITM. Two triggers matter: **short ITM calls the day before ex-dividend** (the
  counterparty exercises to capture the dividend — you get assigned, ending up short stock and owing
  the dividend), and **deep-ITM shorts near expiry**. Manage or close short ITM options before
  ex-dividend; do not be surprised by shares (long or short) appearing in your account.
- **Pin risk at expiry.** A short option sitting right at the strike into expiration may or may not be
  assigned — you find out after the close, carrying unhedged stock over the weekend. Close short
  options near the money before expiration rather than gambling on the pin.
- **PDT (Pattern Day Trader) rule.** In the US, an account under `$25,000` that makes **4+ day trades
  in 5 business days** is flagged PDT and restricted. It constrains how actively you can open/close in
  small accounts — plan trade cadence around it, and prefer positions you are not forced to
  day-trade.
- **Settlement & assignment cash.** Ensure you have the cash/shares to handle an assignment (a
  cash-secured put means actually having the cash). Getting assigned without the capital triggers a
  margin call.

---

## Key takeaways

- **Size by max loss, not premium:** risk 1–2% of equity per trade; contracts = (equity × risk%) ÷
  `|max_loss|`, rounded down. This one rule keeps you solvent.
- **Set portfolio greek limits** (net delta/vega especially) when calm and enforce them when not — a
  book of good trades can still be one giant correlated bet.
- **Diversify** across underlyings, expirations, strategy types, and entry time so no single day or
  regime is a portfolio max-loss event.
- **Liquidity is a veto**, and **earnings/events are avoided by default** or traded only defined-risk.
- **Journal every trade** (template above) and review weekly; run the **entry and exit checklists**
  every time — the plan is written *before* entry.
- **Manage the trader:** loss aversion, revenge trading, overtrading, and FOMO are defeated by
  written rules, a visible journal, and fixed sizing — not willpower.
- **Know the plumbing:** margin/buying-power effects, early assignment around ex-dividend, pin risk,
  and the PDT rule — surprises here cost real money.

## In the next module

The capstone puts all of it into a 30-day paper-trading program with a written trading plan — the
graduation requirement. You will size with these rules, journal with this template, and manage with
these checklists, on real (paper) trades across the strategy families you have learned.
