# SPEC — `optionslab` Strategy Creation & Analyzer Tool

## Purpose

One engine that answers, for any option structure: *what does this position do — now, at expiry,
and under any price/time/vol scenario?* v1 is a Python library used throughout the curriculum.
Later versions add live data, a UI, and backtesting on top of the same core.

## Conventions (binding for all code)

- **Time** is in **years** (`45/365` for 45 DTE). `t = 0` means at expiry (intrinsic value).
- **Vol** is annualized and decimal (`0.25` = 25%). **Rates/yields** decimal annualized.
- **Quantity** sign carries direction: `+` long, `-` short. Options are in contracts with
  `multiplier` (default 100); stock in shares.
- **Premium** is the entry option price **per share**, always ≥ 0; direction comes from quantity.
- **P&L and analyzer outputs are in dollars** for the whole position (premium × multiplier ×
  quantity aggregated). `net_premium() > 0` is a **debit** (cash paid), `< 0` a credit.
- **Max loss is reported as a negative P&L number**; unbounded values are `±math.inf`.
- Greeks conventions: `theta` per **calendar day**, `vega` per **1 vol point** (IV +0.01),
  `rho` per **1% rate move**. Position greeks are aggregated in dollars-per-unit like P&L.
- Every public function has a docstring with formulas/conventions; the docstrings in the source
  stubs are the contract — implementations must match them, and `tests/` is the acceptance suite.

## v1 — Core library (built now)

### `optionslab.pricing`
`bsm_price`, `binomial_price` (CRR, American or European), `implied_vol` (Brent solver with
bracketing; raises `ValueError` when no vol reproduces the price). Handles `t=0` and deep
ITM/OTM edge cases.

### `optionslab.greeks`
`Greeks` dataclass (`delta, gamma, theta, vega, rho`, addable and scalable);
`bsm_greeks` analytic; `numeric_greeks` finite-difference fallback for any pricer;
`position_greeks` aggregates across legs, honoring per-leg time remaining.

### `optionslab.position`
`OptionLeg(kind, strike, expiry, quantity, premium, multiplier=100)`,
`StockLeg(quantity, entry_price)`, immutable `Position(legs, label)` with `net_premium()`,
`option_legs`/`stock_legs` helpers, and `Position.describe()` human-readable summary.

### `optionslab.payoff`
`payoff_at_expiry` (intrinsic-value liquidation; documented caveat for mixed expiries),
`pnl_at_expiry`, `pnl_at(position, spot, t_elapsed, vol, …)` mark-to-model via BSM (this is what
calendars/diagonals require), `pnl_curve` vectorized over spots.

### `optionslab.strategies`
Factory functions returning labeled `Position`s. Uniform convention: **every option leg is a
`(strike, premium)` tuple**; shared `expiry` (in years) and `quantity` (structures) parameters;
time spreads take per-leg expiries. Catalog (v1):
long_call, long_put, covered_call, cash_secured_put, protective_put, collar,
bull_call_spread, bear_put_spread, bull_put_spread, bear_call_spread,
long_straddle, short_straddle, long_strangle, short_strangle,
iron_condor, iron_butterfly, long_call_butterfly, long_put_butterfly,
calendar_spread, diagonal_spread, poor_mans_covered_call,
call_ratio_spread, put_ratio_spread, call_backspread, put_backspread,
broken_wing_butterfly, jade_lizard, custom (from raw legs).

### `optionslab.analyzer`
- `breakevens(position)` — zeros of expiry P&L, found numerically on an adaptive spot grid.
- `max_profit(position)` / `max_loss(position)` — over expiry payoff; `±inf` when unbounded
  (detected from boundary slopes).
- `probability_of_profit(position, spot, vol, …)` — lognormal terminal distribution at the
  position's earliest expiry, numeric integration of the profit region.
- `expected_move(spot, vol, t)` — 1σ move helper.
- `scenario_grid(position, spots, days_forward, vol | vols, …)` — tidy `DataFrame` of
  mark-to-model P&L across price × time (or price × vol): the adjustment-training engine.
- `summarize(position, spot, vol, …)` — dict: net premium/credit, breakevens, max P/L, POP,
  expected move, current position greeks.

### `optionslab.viz`
Matplotlib: `plot_payoff` (expiry line + optional "now" mark-to-model curve, breakevens, current
spot), `plot_greeks` (greek curves vs spot), `plot_pnl_heatmap` (scenario grid), `plot_compare`
(overlay payoff of several candidate structures). All take/return `Axes` for composability.

### `optionslab.data`
`load_sample_chain(name)` → DataFrame from `data/samples/*.csv`
(columns: `kind, strike, expiry_days, bid, ask, mid, iv, volume, open_interest, spot`);
`list_sample_chains()`; `fetch_chain(ticker, expiry=None)` via optional `yfinance` import with a
helpful error if unavailable. The curriculum only requires the offline samples.

### Quality bar
- `pytest` green: reference BSM values, put-call parity, binomial↔BSM convergence, greeks vs
  finite differences, IV round-trip, per-strategy breakevens/max-P&L, POP sanity, grid shape.
- Pure functions, no I/O in core modules, numpy-vectorized where natural, type hints throughout.

## Future phases (spec'd, not built in v1)

### v2 — Live chain analysis & screener
Real chains via `yfinance` behind the same `data` interface; compute IV rank/percentile from
price history; expected-move vs priced-move comparison; a screener that ranks candidate
structures from the module-08 selection matrix given a ticker's current regime.

### v3 — Streamlit strategy builder UI
Interactive leg builder (chain picker → click strikes), live payoff/greeks panels from the v1
analyzer, side-by-side structure comparison, save/load positions (JSON), an "adjustment
sandbox" that wraps `scenario_grid`.

### v4 — Backtester
Historical simulation of the module-08 matrix rules and module-09 management rules (entry DTE,
delta targets, profit-take/stop levels, 21-DTE management) over daily data; per-strategy
statistics (win rate, expectancy, max drawdown). Data source pluggable; start with yfinance dailies
and synthetic IV.
