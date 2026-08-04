# 03 — Single Legs and Stock Combinations

Phase 1 taught you to *read* the machine; Phase 2 teaches you to *build* with it. This is the
first strategy module, and it starts where every options trader's real P&L starts: the six
structures that use one option, or one option bolted onto stock. Long call, long put, covered
call, cash-secured put, protective put, collar. They are not "beginner" strategies you graduate
away from — professionals run covered calls and cash-secured puts on nine-figure books. They are
the foundation because they teach the two lessons the whole rest of the curriculum elaborates:
**buying options fights time and vol; selling options harvests them.**

From here on, every strategy gets a **strategy card** in the exact structure of `TEMPLATE.md`:
construction, payoff/greeks profile, when to use it (direction × IV × horizon), entry criteria,
management, exits, common mistakes. Learn to think in that card. By module 05's exit gate you must
be able to recite it from memory for fourteen structures.

We build every example on **DEMO**: spot **$100**, IV **~25%**, the **45-DTE** expiration, using
the real chain mids you saw in module 00.

---

## The two families

Before the cards, the organizing idea. These six split cleanly:

**Debit / long-premium (you pay):** long call, long put, protective put. You *buy* optionality.
Time decay (theta) works **against** you; you are **long vega** (falling IV hurts). You need the
stock to *move*, and move *more than the premium and decay cost you*. These fit **low-IV**
environments and higher-conviction directional views.

**Credit / short-premium (you collect):** covered call, cash-secured put. You *sell* optionality.
Time decay works **for** you; you are **short vega** (falling IV helps). You profit if the stock
does *not* move much against you. These fit **high-IV** environments and neutral-to-moderate
directional views. The **collar** is a hybrid — long stock, wrapped in a bought put and a sold
call.

Keep module 02's rule bolted on: *buying options in high IV and selling them in low IV are both
uphill battles.* Match your vega sign to the IV regime.

---

## Strategy card — Long Call

**Construction.** Buy one call. On DEMO: buy the 100 call, 45 DTE, for **3.91** (a $391 debit per
contract). `strategies.long_call((100, 3.91), expiry=45/365)`.

**Payoff & greeks profile.** Loss capped at the premium paid ($391); profit theoretically
unlimited above the strike. Breakeven at expiry = **strike + premium = 103.91**. You are **long
delta** (bullish, ~+0.53 at entry, rising toward +1 as it goes ITM — positive gamma helps on the
way up), **long vega** (rising IV inflates the option), and **short theta** (you bleed time value
daily — the rent).

**When to use it.** Direction: **bullish**, with real conviction and a *catalyst or timeframe* in
mind — you need a move, not a drift. IV: **low** (low IV rank) so you are not overpaying for vega;
buying a call into rich IV means the stock can rise and you still lose to the vol crush. Horizon:
enough DTE that theta does not gut you before your thesis plays out — for a swing view, 45–90 DTE
is far kinder than a 7-DTE lottery ticket.

**Entry criteria.** Pick a strike by how much conviction and leverage you want: ATM (100, ~0.50
delta) balances cost and responsiveness; slightly ITM (95, higher delta) behaves more like stock
with less time-decay drag as a fraction of premium; OTM (105+) is cheaper but needs a bigger move
and decays faster in percentage terms. Buy enough time — a common rule is *at least* 45 DTE for a
directional swing so decay is gentle at first. Liquidity: tight spread, real OI (module 00).

**Management & adjustment.** Because theta is against you, **do not marry a long option.** If the
thesis plays out and you are up ~50–100%, take profits — the remaining extrinsic value is now
working against you. If it moves your way hard, consider *rolling up* (sell the ITM call, buy a
higher strike) to lock gains and reduce capital at risk. If IV spiked in your favor, some of your
gain is vega, not delta — take it before it mean-reverts.

**Exit rules.** Time-stop *and* price-stop. Never let a long option ride into the last ~1–2 weeks
hoping — that is where decay is brutal; close or roll out by ~21 DTE if the move has not happened.
Set a loss limit (e.g., cut at −50% of premium) so a wrong thesis costs you a fraction, not the
whole ticket.

**Common mistakes.** Buying too little time (weeklies as "cheap" bets — they are decay bombs);
buying calls into high IV (right on direction, killed by vol crush); buying too far OTM chasing
leverage; and sizing by premium instead of by the real probability of a total loss — a call has a
very real chance of expiring worthless.

---

## Strategy card — Long Put

**Construction.** Buy one put. On DEMO: buy the 100 put, 45 DTE, for **3.42** ($342 debit).
`strategies.long_put((100, 3.42), expiry=45/365)`.

**Payoff & greeks profile.** Loss capped at premium ($342); profit large (capped only because a
stock cannot fall below 0) down to breakeven = **strike − premium = 96.58**. You are **short delta**
(bearish, ~−0.47 at entry, toward −1 as it goes ITM), **long vega**, **short theta**. The mirror
of the long call, pointed down.

**When to use it.** Direction: **bearish** with conviction and a timeframe, *or* as a hedge on a
long stock position (that specific use is the protective put, below). IV: **low** for a
speculative bearish bet — but note the module-02 skew means puts are *structurally* richer than
calls, so downside is rarely "cheap"; you often pay up for the put skew. Horizon: like the call,
buy time — 45+ DTE.

**Entry criteria.** Strike by conviction: ATM for balance, OTM for cheaper/bigger-move bets. Mind
the skew — the OTM put you want carries elevated IV, so quantify what you are paying. Liquidity as
always.

**Management & adjustment.** Same discipline as the long call: take profits into a sharp down-move
(the extrinsic value that remains is decay risk); roll down to lock gains if it craters; cut on a
wrong thesis. Puts often *gain vega* in a selloff (IV rises when stocks fall) — a pleasant tailwind,
but recognize part of the gain is vega and can reverse.

**Exit rules.** Time-stop by ~21 DTE; price-based profit target and loss limit. Do not hold a
speculative put into the last week for a miracle.

**Common mistakes.** Overpaying for skew-inflated OTM puts; using long puts as a *permanent* hedge
(the bleed is real — a protective put every month is expensive insurance; see the collar for a
cheaper structure); and, again, too little time.

---

## Strategy card — Covered Call

**Construction.** Own 100 shares; sell one OTM call against them. On DEMO: long 100 shares at
**100** (\$10,000), sell the 105 call, 45 DTE, for **1.85** (collect \$185).
`strategies.covered_call(100, (105, 1.85), expiry=45/365)`.

**Payoff & greeks profile.** This is the income workhorse. The short call caps your upside at the
strike but pays you a credit for the cap. Max profit = (strike − stock cost) + premium =
(105 − 100) + 1.85 = **6.85** ($685), realized if the stock is ≥ 105 at expiry (you sell your
shares at 105 and keep the premium). Downside is the stock's — you still own 100 shares — but
*cushioned* by the 1.85 credit: your breakeven drops to **100 − 1.85 = 98.15**. Greeks: net
**long delta** but *less* than pure stock (the short call subtracts delta), **positive theta**
(you now *earn* decay), **short vega** (falling IV helps you), **short gamma** from the call.

**When to use it.** Direction: **neutral to mildly bullish** — you are willing to own the stock and
happy to sell it at the strike. If you are wildly bullish, the cap will frustrate you; if you are
bearish, do not own the stock at all. IV: **high** IV rank makes the call you sell fat — you collect
more premium for the same cap. Horizon: 30–45 DTE is the sweet spot (rich theta, manageable gamma),
repeated monthly.

**Entry criteria.** Own (or buy) 100 shares per call. Choose the short strike by how much upside you
will surrender: a ~30-delta OTM call (here ~105–107) is a common balance — meaningful premium,
room to appreciate. A higher strike = more upside kept, less premium; ATM = most premium, least
upside. Sell into elevated IV.

**Management & adjustment.** The classic rule: **buy the short call back at ~50% of the credit**
and re-sell a new one (harvest most of the decay, reset). If the stock rips through your strike and
you do not want to lose the shares, **roll the call up and out** (buy back, sell a higher strike in
a later month) — ideally *for a credit*. If assignment approaches on a dividend stock and the call
is ITM with little extrinsic value left, expect early assignment before ex-date (module 00) — roll
or accept it. If the stock drops, the call decays to your benefit, cushioning the loss; you keep
the shares and can sell another call next cycle.

**Exit rules.** Let it ride to expiration to capture full decay if the stock stays below the strike;
or take it off at 50% early. If ITM at expiration, you are assigned and sell your shares at the
strike — often a *feature*, not a bug: you sold stock at your target price and got paid to wait.

**Common mistakes.** Selling calls on a stock you are not willing to sell (then panic-buying-back
the call in a rally, turning income into a loss); selling too close (ATM) and capping all upside on
a name you are bullish on; ignoring the *downside* (the covered call does **not** protect you much —
a $185 credit is thin cushion against a 20% drop; you are still long 100 shares); and selling into
low IV for scraps of premium.

---

## Strategy card — Cash-Secured Put

**Construction.** Sell one OTM put; set aside the cash to buy the stock if assigned. On DEMO: sell
the 95 put, 45 DTE, for **1.58** (collect \$158), with \$9,500 reserved.
`strategies.cash_secured_put((95, 1.58), expiry=45/365)`.

**Payoff & greeks profile.** The bullish mirror of the covered call (near-identical payoff by
put-call parity). Max profit = the premium, **1.58** ($158), kept if the stock stays above 95 at
expiry. If assigned, you buy 100 shares at 95 — but your *effective* cost basis is 95 − 1.58 =
**93.42**, a discount to today's 100. Breakeven = **93.42**. Risk is real and large: if the stock
craters to 70, you are assigned at 95 and own a stock worth 70 (loss cushioned only by the 1.58).
Greeks: **positive delta** (bullish), **positive theta**, **short vega**, short gamma.

**When to use it.** Direction: **neutral to bullish** on a stock you *genuinely want to own* at the
strike. This is the key mindset — a cash-secured put is "get paid to place a limit buy order below
the market." IV: **high** IV rank fattens the premium. Horizon: 30–45 DTE, monthly.

**Entry criteria.** Only on stocks you are happy to own. Pick the short strike at a price you would
gladly buy — often a ~30-delta or ~16-delta OTM put (here ~95 or lower). Secure the full cash
(strike × 100) so assignment is not a margin event. Sell into elevated IV.

**Management & adjustment.** **Take profit at ~50%** of the credit and re-sell, same as the covered
call. If the stock falls toward the strike and you *still* want the shares, let assignment happen —
then you own stock at a discount and can start selling covered calls against it (this
put-then-call loop is the **"wheel"**). If you *no longer* want the shares (thesis changed), **roll
the put down and out for a credit** to defend. Watch for early assignment on deep-ITM puts (rare,
carry-driven).

**Exit rules.** Let it expire worthless above the strike (keep full premium) or close at 50% early.
If ITM at expiration, accept assignment (a feature if you wanted the stock) or roll.

**Common mistakes.** Selling puts on stocks you would *hate* to own (the premium is not worth
catching a falling knife); not securing the cash (naked puts on margin can force liquidation);
selling too close to the money on a name that then gaps down; and treating the credit as "free
money" while ignoring that your max loss is *(strike − premium) × 100* — a lot.

---

## Strategy card — Protective Put

**Construction.** Own 100 shares; buy a put as insurance. On DEMO: long 100 shares at **100**, buy
the 95 put, 45 DTE, for **1.58** (pay \$158). `strategies.protective_put(100, (95, 1.58),
expiry=45/365)`.

**Payoff & greeks profile.** A floor under your stock. Below the put strike you are fully hedged —
losses stop at the strike. Max loss = (stock cost − put strike) + premium = (100 − 95) + 1.58 =
**6.58** ($658), no matter how far the stock falls. Upside is the stock's, minus the premium drag:
breakeven = **100 + 1.58 = 101.58**. Greeks: **long delta** (still bullish, but the put subtracts
some), **long vega** (the put you own gains if IV rises — a selloff tailwind), **short theta** (you
pay for the insurance daily).

**When to use it.** Direction: **bullish but nervous** — you want to hold the stock (or must, for
tax/other reasons) but cannot stomach a crash. It is insurance: you pay a premium to cap downside.
IV: cheaper to buy protection when IV is **low**; buying puts in high IV is expensive insurance
(and remember the put skew). Horizon: match the window you are worried about (an earnings print, a
macro event).

**Entry criteria.** Choose the put strike = your pain threshold (the 95 put floors a 5% drawdown +
premium). Closer-to-money puts protect more but cost more; further-OTM puts are cheaper "disaster"
insurance. Size one put per 100 shares.

**Management & adjustment.** Insurance decays — do not overpay for it perpetually. If the stock
rises, the put loses value (that is fine; your shares gained more); you can roll the put up to lock
in some stock gains and re-strike the floor. If the stock falls and the put goes ITM, you are
protected; decide whether to sell the appreciated put (and re-hedge lower) or exercise. A recurring
protective put is expensive — which is exactly why the **collar** exists.

**Exit rules.** Tie the put's life to the risk window; close/roll it when the worry passes. If the
stock tanks, the put has done its job — monetize it.

**Common mistakes.** Buying protection *after* the scare (when IV — and put skew — are already
elevated, so insurance is dear); over-insuring (a tight ATM put every month can cost more than the
crashes it prevents); and forgetting the premium drag raises your breakeven.

---

## Strategy card — Collar

**Construction.** Own 100 shares; buy a protective put *and* sell a covered call to finance it. On
DEMO: long 100 shares at **100**, buy the 95 put for **1.58**, sell the 105 call for **1.85** — a
net **credit of 0.27**. `strategies.collar(100, (95, 1.58), (105, 1.85), expiry=45/365)` (requires
put strike < call strike).

**Payoff & greeks profile.** A *banded* stock position: the put floors your downside, the sold call
caps your upside, and the call's premium pays for (here, more than pays for) the put. Max loss =
(stock cost − put strike) − net credit = (100 − 95) − 0.27 = **4.73** ($473). Max profit =
(call strike − stock cost) + net credit = (105 − 100) + 0.27 = **5.27** ($527). You have boxed the
outcome into a tidy range for near-zero cost. Greeks: **long delta** but muted on both ends;
theta and vega roughly wash between the long put and short call; you have traded away tail
exposure in both directions.

**When to use it.** Direction: **neutral, protective** — you own a stock (often with a gain you do
not want to sell yet), you want crash protection, and you are willing to cap upside to get it
cheaply. Extremely common for concentrated positions and around events. IV: skew *helps* you here —
selling the (relatively cheaper-vol) call to buy the (richer-vol) put still often nets a credit
because the call strike sits where you are happy to sell. Horizon: event window or monthly.

**Entry criteria.** Put strike = your downside floor; call strike = the price you will happily sell
at; aim for a **zero-cost or credit** collar by choosing strikes so the call premium ≥ the put
premium. Wider band = more room but less protection/financing; tighter band = safer but caps gains
sooner. One put and one call per 100 shares (put strike < call strike, enforced by the factory).

**Management & adjustment.** If the stock rises to the call, you are assigned and sell at the cap
(a feature — you locked a good exit). If it falls to the put, you are floored. Roll the whole collar
up in a rally to raise both the floor and the cap; roll the call out for more credit if you want to
keep the shares. As with the covered call, watch dividend early-assignment on the short call.

**Exit rules.** Let the band resolve at expiration (assigned up, floored down, or somewhere in
between and re-collar next cycle), or unwind early if the reason for hedging passes.

**Common mistakes.** Setting the call strike below where you are actually willing to sell (you cap a
stock you wanted to ride); collaring so tightly there is no room to make anything; and forgetting
that, like the covered call, a collar means you *will* give up the shares in a big rally — the price
of the cheap protection.

---

## Covered call vs. plain stock: the trade you are actually making

Put the covered call beside owning 100 shares outright and you see the whole bargain. Below the
strike, the covered call *outperforms* stock by the premium collected (that 1.85 cushion). At and
above the strike, stock keeps climbing while the covered call flatlines at its cap. **You have sold
your upside tail for a certain, immediate credit.** In flat, choppy, or mildly-up markets — where
stocks spend most of their time — the covered call wins. In a rip-your-face-off rally, plain stock
wins. That trade-off, made deliberately and repeatedly into elevated IV, is why covered calls are
an income *workhorse* and not a free lunch. The notebook plots these two payoff curves on the same
axes so you can see exactly where they cross.

---

## Key takeaways

- **Two families.** Long call / long put / protective put are **debit, long-vega, short-theta** —
  they fight time and vol, need a move, and fit **low IV** and conviction. Covered call /
  cash-secured put are **credit, short-vega, long-theta** — they harvest time and vol, profit from
  *not* moving against you, and fit **high IV**.
- **Long options: buy time and take profits.** Too little DTE and buying into high IV are the two
  classic ways to be right and still lose. Cut losers, bank winners near +50–100%, roll by ~21 DTE.
- **Covered call and cash-secured put are the same trade in two costumes** (put-call parity):
  bullish-to-neutral, sell rich premium, manage at **50% profit**, treat assignment as a *feature*
  (sell high / buy at a discount). The **wheel** loops them.
- **Neither the covered call nor the CSP protects the downside much** — the credit is a thin
  cushion, not a hedge. Your CSP max loss is *(strike − premium) × 100*.
- **Protective put** is insurance (long vega, pays theta); the **collar** finances that insurance
  by capping upside — often for a net *credit*, with the skew working in your favor.
- Always place yourself on **direction × IV** first (module 02): the same view is a *long call* in
  cheap vol and a *cash-secured put* in rich vol.

## In the next module

We add a second option leg to define risk precisely: **vertical spreads** — bull call, bear put,
and the credit verticals — where strike width, the debit-vs-credit choice, and the
probability/reward trade-off all become dials you set on purpose.
