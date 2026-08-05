# TODO — Master Tracker

Two tracks: **Learning** (your progress through the curriculum) and **Build** (the tool).
Check items off as you go; this file is yours to edit.

## Learning track

### Phase 1 — Foundations
- [ ] 00-foundations: lesson + notebook + exercises
- [ ] 01-greeks: lesson + notebook + exercises
- [ ] 02-volatility: lesson + notebook + exercises
- [ ] **Exit gate 1 passed** (chain-reading drill)

### Phase 2 — Core strategies
- [ ] 03-single-leg-and-stock
- [ ] 04-vertical-spreads
- [ ] 05-neutral-income
- [ ] Paper-trading started (≥1 position, journaled)
- [ ] **Exit gate 2 passed** (blind strategy table)

### Phase 3 — Complex structures & regime selection
- [ ] 06-time-spreads
- [ ] 07-advanced-structures
- [ ] 08-market-conditions
- [ ] **Exit gate 3 passed** (10 scenario drills)

### Phase 4 — Management & mastery
- [ ] 09-adjustments
- [ ] 10-risk-and-best-practices
- [ ] 11-capstone: 30-day paper program
- [ ] **Exit gate 4 passed** (trading plan + reviewed journal)

## Build track

### v1 — Core library (this repo, initial build)
- [x] Architecture, SPEC, ROADMAP, repo skeleton
- [x] API stubs with docstring contracts
- [x] Acceptance test suite
- [x] `pricing` / `greeks` / `position` / `payoff` implementation
- [x] `strategies` catalog
- [x] `analyzer` (breakevens, max P/L, POP, scenario grid, summarize)
- [x] `viz` plots
- [x] `data` sample chains + loader
- [x] Curriculum modules 00–11 (lesson + notebook + exercises each)
- [x] All tests green; all notebooks execute offline

### Russian edition (`curriculum-ru/`)
- [x] Modules 00–11 translated (lesson + notebook + exercises each)
- [x] `ROADMAP.ru.md`, `README.ru.md`, language switcher in `README.md`
- [x] All 12 Russian notebooks execute offline; executable code verified
      identical to the English originals (only prose/comments/labels differ)

### v2 — Live chains & screener (next project — see SPEC.md)
- [ ] `fetch_chain` hardened against real yfinance data
- [ ] IV rank / percentile from price history
- [ ] Expected-move vs priced-move report
- [ ] Selection-matrix screener

### v3 — Streamlit builder UI
- [ ] Leg builder on top of chain picker
- [ ] Live payoff/greeks panels
- [ ] Structure comparison + save/load (JSON)
- [ ] Adjustment sandbox (scenario_grid UI)

### v4 — Backtester
- [ ] Daily-bar simulation engine
- [ ] Strategy rule encoding (entry DTE, delta targets, profit take, 21-DTE management)
- [ ] Per-strategy statistics report
