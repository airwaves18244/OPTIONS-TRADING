# 08 — Market Conditions: The Strategy Selection Matrix

You now own a large toolbox: single legs, verticals, condors and flies, calendars and diagonals,
ratios, backspreads, broken wings, jade lizards. This module is the one that turns a toolbox into a
craft. The professional does not ask "what's my favorite strategy?" — they ask, in order: *which way
do I lean, how expensive is volatility right now, and how long is my horizon?* Those three answers
land you in a cell of a matrix, and the matrix hands you two or three candidate structures. Then
tie-breakers — liquidity, account size, events, assignment tolerance — pick the winner. After this
module you can take any market setup and reason, out loud and in the matrix's terms, to a defensible
structure. That skill is exit gate 3, and it is the whole point of everything before it.

---

## The three axes

### Axis 1 — Direction

Where do you think the underlying goes over your horizon: **bullish**, **bearish**, or **neutral**
(range-bound, no strong lean)? Be honest about *conviction*, too: "mildly bullish, could stall" is a
different cell from "convinced it breaks out." Conviction sets how directional (how much delta) you
want and whether you prefer a debit bet or a premium-collecting range trade around your bias. A
high-conviction bull buys a call or a debit spread and wants delta; a low-conviction, "grinds higher
or chops" bull is often better served *selling* a put spread below the market — you profit if the
stock rises, stalls, or even drifts down modestly, a far wider win zone than an outright directional
bet. The direction axis is therefore two questions: which way, and *how sure* — and the second one
frequently moves you from buying direction to selling premium around it.

### Axis 2 — IV level (the pivot)

This is the axis beginners skip and professionals lead with. From module 02: **IV rank / IV
percentile** tells you whether implied vol is high or low *relative to this underlying's own
history*. It decides whether you should be a **net buyer** or **net seller** of options:

- **High IV (rank ≳ 50, especially ≳ 70):** options are expensive; **sell premium**. Favor credit
  structures — credit verticals, iron condors, iron butterflies, strangles, jade lizards, ratios.
  You want IV to *fall* (vega short) and time to pass (theta long).
- **Low IV (rank ≲ 30):** options are cheap; **buy premium** or use debit/long-vega structures —
  long options, debit verticals, calendars/diagonals (long back-month vega), backspreads. You want
  IV to *rise* and you accept paying theta.

The mantra: **sell high IV, buy low IV.** Fighting this — buying options when they are expensive,
selling when they are cheap — is the uphill battle module 03 warned about.

Two refinements keep this axis honest. First, **IV rank is relative to the underlying's own
history**, not to other stocks: a biotech at 55% IV can be *cheap* (rank 20) while a utility at 18%
is *rich* (rank 80). Never eyeball the absolute IV number and call it high or low — pull the rank.
Second, IV rank tells you *which side* to be on, but it does not by itself tell you the trade will
work: a high IV rank often reflects real, elevated risk (an event, a downtrend), and selling into it
still loses if the feared move happens. IV rank sets your *posture* (buyer vs seller); the direction
and regime axes decide whether you should have a position at all. A useful discipline: pair the IV
read with the **expected move** (`analyzer.expected_move` — roughly `spot × IV × sqrt(t)`). If the
market's priced move comfortably contains your break-evens, a premium sale has room; if your
structure's break-evens sit *inside* one expected move, you are being paid too little for the risk.

### Axis 3 — Horizon (and events)

How long until you expect your thesis to play out, and what is on the calendar? Horizon sets **DTE**
and interacts with theta and gamma:

- **Short horizon / near-dated (≤ ~21 DTE):** fast theta but violent gamma. Great for harvesting
  decay if you are a disciplined seller; dangerous to hold short premium into.
- **Medium (30–60 DTE):** the sweet spot for most premium selling — enough theta, gamma still
  manageable. The default for condors, credit spreads, calendars.
- **Long (60–180+ DTE):** for directional debit trades, PMCCs, and LEAPS-style positions where you
  want time for a thesis and less gamma sensitivity.
- **Events (earnings, Fed, data):** an event inside your horizon inflates front-month IV and creates
  crush opportunities *and* gap risk. Either trade the event deliberately (sell the crush with
  defined risk, or buy convexity if you think the move is under-priced) or **avoid** holding
  undefined risk through it.

---

## The selection matrix

Read it as: **your directional lean (rows) × the IV environment (columns)**. Each cell lists primary
candidate structures; horizon and the tie-breakers below narrow to one. "Debit" trades want low IV;
"credit" trades want high IV — notice how the columns sort themselves.

| Direction ↓ / IV → | **Low IV (rank ≲ 30) — buy premium** | **High IV (rank ≳ 50) — sell premium** |
|---|---|---|
| **Bullish (high conviction)** | Long call; bull **call** (debit) spread; call **backspread** (expect a big move) | Short/cash-secured put; bull **put** (credit) spread; **jade lizard** |
| **Bullish (mild / patient)** | Long-dated debit call spread; **call diagonal**; **PMCC** | Bull put spread (further OTM); covered call; **put ratio** (target-price) |
| **Bearish (high conviction)** | Long put; bear **put** (debit) spread; put **backspread** | Bear **call** (credit) spread; short call spread; **call ratio** (target) |
| **Bearish (mild / patient)** | Put **calendar/diagonal** below market; long-dated debit put spread | Bear call spread (further OTM); **broken-wing** call fly skewed down |
| **Neutral (range / pin)** | **Calendar** at the pin; long **butterfly** (cheap, defined) | **Iron condor**; **iron butterfly**; **short strangle**; **BWB** |
| **Neutral but expecting a BIG move (long vol)** | **Long straddle / strangle**; backspreads | *(rarely right in high IV — you'd be buying dear vol; prefer waiting or a calendar)* |
| **Explicit volatility view (vol up)** | Long straddle/strangle; **calendar** (long back vega) | — (high IV already; buying vol is expensive) |
| **Explicit volatility view (vol down / crush)** | — | **Short strangle/straddle**; iron condor; sell the **earnings** front |

Two structural notes the matrix encodes:

1. **The debit/credit choice is an IV decision, not a preference.** The same bullish view is a bull
   *call* spread in low IV and a bull *put* spread in high IV. Pick the column first.
2. **Neutral splits by what kind of neutral.** "Range-bound and quiet" wants short premium in high IV
   (condor) or a cheap defined fly/calendar in low IV. "Coiled, about to move, direction unknown"
   wants *long* vol (straddle/strangle/backspread) — and that is far easier to justify when IV is
   low.

---

## Tie-breakers (how you pick within a cell)

The matrix narrows you to two or three candidates; these decide the winner.

- **Liquidity.** Tight bid/ask, real volume and open interest. A theoretically perfect four-leg
  condor in an illiquid name loses its edge crossing four wide spreads. Prefer fewer legs and
  penny-wide markets. *Liquidity can veto the "best" structure.*
- **Account size & buying power.** Defined-risk structures (spreads, condors, flies) cap capital and
  margin; naked/undefined structures (short strangles, ratios, cash-secured puts) demand more buying
  power and can be off-limits or unwise in a small account. Size every position by **max loss**
  (module 10), not premium.
- **Events on the calendar.** Earnings/Fed inside the horizon: either the trade *is* the event play
  (defined risk) or you pick an expiry that avoids it. Never hold an undefined-risk short through
  earnings by accident.
- **Assignment tolerance.** Would you be fine owning (or shorting) the stock at the short strike? If
  yes, cash-secured puts / covered calls / jade lizards are comfortable. If you cannot take
  assignment (no capital, IRA rules, don't want the shares), stay defined-risk and manage before
  expiry; watch ITM shorts around ex-dividend.
- **Skew.** Puts usually trade richer than calls. That subtly favors put-selling structures on the
  downside and makes call-side credit thinner — factor it when the matrix offers a put-side vs
  call-side choice.

These tie-breakers are not a tiebreak of last resort — they routinely *override* the "textbook best"
structure. A theoretically ideal short strangle in an account that cannot margin undefined risk is
simply not available; a beautiful four-leg condor in an illiquid name loses to a two-leg spread in a
liquid one; a jade lizard is the wrong trade for someone who cannot stomach owning the stock on a
drop. Run the axes to get candidates, then run the tie-breakers *as hard filters* — anything that
fails liquidity, exceeds your buying power, or commits you to an outcome you cannot accept is off the
table regardless of how good the payoff diagram looks.

---

## Regimes: which matrix are you even in?

The matrix assumes you have correctly read direction and IV. Two higher-level reads set that up:

**Trending vs ranging.** In a **trending** market (higher highs / higher lows, price riding a moving
average), mean-reversion range trades — condors, short strangles — get run over; favor
*directional* or *trend-following* structures (debit spreads with the trend, diagonals, PMCCs,
put-credit spreads under an uptrend). In a **ranging** market (price oscillating between support and
resistance, no slope), the neutral premium-sellers shine: sell the range's edges. Misclassifying a
trend as a range is how condor sellers get hurt — a trend looks like a series of "it's overbought,
it'll revert" signals right up until it takes out your short strike. Practical tells: is price above
or below a rising/falling medium-term average? Are pullbacks getting bought (uptrend) or rallies
sold (downtrend)? Is the range's width stable, or expanding? When in doubt, treat a market as
trending until it proves it is ranging — the cost of fading a real trend is larger than the cost of
missing a chop.

**Volatility regime.** Beyond a single name's IV rank, the broad vol environment (think of a VIX-like
gauge) sets the backdrop. In a **low-vol, calm regime**, premium is thin and mean-reversion works;
in a **high-vol, stressed regime**, premium is fat but moves are large and correlations spike — size
down, widen wings, and respect that "high IV rank" in a crisis can go higher still. Vol clusters:
calm follows calm, storms follow storms.

**Event calendars.** Keep a standing list for every underlying you trade: earnings date, ex-dividend
date, and macro events (Fed, CPI, jobs). These reshape IV term structure (module 06) and create the
crush/gap dynamics that decide whether a given expiry is a gift or a trap.

---

## The selection workflow (use this every time)

1. **Regime:** trending or ranging? calm or stressed vol? Any event inside my horizon?
2. **Direction:** bullish / bearish / neutral, and how strong is my conviction?
3. **IV level:** IV rank high or low — am I a net seller or net buyer?
4. **Horizon → DTE:** pick the expiry (avoid or embrace events deliberately).
5. **Matrix cell → candidates:** list the 2–3 structures the cell offers.
6. **Tie-breakers:** liquidity, account/margin, assignment tolerance, skew → pick one.
7. **Pre-trade check (the notebook):** build the finalists, compare `summarize` +
   `viz.plot_compare`, confirm max loss, POP, breakevens, and greeks match the view. Trade the one
   whose numbers best fit — and write down the entry, target, and adjustment plan *before* sending.

---

## A worked example (the workflow end to end)

Suppose HIGHVOL (spot 62) has just finished a scary week: it sold off, then stabilized, and IV rank
is now ~78. You have no strong directional view — it feels like it will chop for a few weeks — and no
earnings are scheduled inside a month. Walk the steps.

1. **Regime:** the sharp sell-off then stall reads *ranging after a shock*, not a fresh trend. Vol
   regime is *stressed* (IV rank 78), so moves can still be large — a flag to size down and widen.
2. **Direction:** neutral, low conviction. That points at the neutral row.
3. **IV level:** IV rank 78 is high → **sell premium**, the high-IV column.
4. **Horizon:** ~30 days, no event → 30 DTE cycle.
5. **Matrix cell (neutral × high IV):** iron condor, iron butterfly, short strangle.
6. **Tie-breakers:** stressed vol + "moves can be large" argues *against* the naked short strangle
   (undefined risk when the tape is violent) and *against* a tight iron butterfly (pin bet into
   chop). The **iron condor** — defined risk, wide profit zone, shorts near the range edges — fits;
   widen the wings a touch for the stressed regime and size to 1–2% max loss.
7. **Pre-trade check:** build the condor and a wider-winged alternative, compare `summarize`
   (credit, POP, max loss, breakevens) and overlay with `viz.plot_compare`, confirm the break-evens
   sit *outside* one expected move, then write the plan (50% profit target, 21-DTE decision, roll the
   untested side if tested) before sending.

Notice that the matrix did most of the work in two reads (neutral, high IV), and the *regime*
(stressed vol) and *tie-breakers* (defined risk, account size) turned three candidates into one. That
is the whole method: narrow fast with the axes, then let the practical constraints break the tie.

## A note on horizon, expected move, and being paid enough

The horizon axis is not just "pick a DTE." It sets how much *time value* you are buying or selling and
how the trade decays. A premium seller wants enough DTE that theta is meaningful (30–45) but not so
much that capital is tied up for a thin annualized return; a premium buyer wants enough time for the
thesis without paying for time the move will not need. Tie it back to the **expected move**: at 30
DTE, HIGHVOL's 1σ move is `62 × 0.55 × sqrt(30/365) ≈ ±$9.8`. A condor whose short strikes sit inside
that ±$9.8 band is likely to be tested; strikes near or beyond it (the ~16Δ neighborhood) give the
range room. The horizon and IV together *define the width you must respect* — ignore the expected
move and you will keep selling ranges the market has already told you are too narrow.

---

## Key takeaways

- Choose structures with a **process**, not a favorite: **direction × IV level × horizon**, then
  tie-breakers.
- **IV rank is the pivot:** high IV → sell premium (credit/short vega); low IV → buy premium
  (debit/long vega). The debit-vs-credit choice *is* the IV decision.
- The matrix gives **candidates**; **liquidity, account size, events, assignment tolerance, and
  skew** pick the winner — and liquidity can veto everything.
- **Neutral splits** into "quiet range" (short premium / cheap fly) vs "coiled, big move coming"
  (long vol) — and the latter is far easier to justify in *low* IV.
- Read the **regime** first: trending markets punish range sellers; ranging markets reward them;
  stressed vol means size down and widen.
- Always finish in the notebook: **build the finalists, compare, and confirm the numbers match the
  thesis** before committing — and write the plan down first.

## In the next module

Choosing well is half the job. Next: **adjustments** — what to do when the market moves against an
open position. The adjust-vs-close framework, rolling for credit, defending tested spreads and
condors, and the 21-DTE decision point. This is where the analyzer earns its keep.
