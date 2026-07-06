# OPTIONS-TRADING — Curriculum + Strategy Lab

A complete, self-paced system for learning options trading, paired with **`optionslab`** — a
Python library for building and analyzing option strategies. The two grow together: every
curriculum module teaches concepts in a Markdown lesson, then makes them concrete in a Jupyter
notebook powered by the library. By the time you finish the curriculum, you also know the tool —
and the tool is the foundation for the future strategy builder/analyzer application.

## What's here

| Path | What it is |
|---|---|
| [`ROADMAP.md`](ROADMAP.md) | The step-by-step learning workflow: phases, modules, exit gates, weekly cadence |
| [`SPEC.md`](SPEC.md) | Specification of the `optionslab` tool (v1 library, and future v2–v4 phases) |
| [`TODO.md`](TODO.md) | Master progress tracker for curriculum and tool |
| [`curriculum/`](curriculum/) | 12 modules, simple → complex. Each has `lesson.md`, `notebook.ipynb`, `exercises.md` |
| [`src/optionslab/`](src/optionslab/) | The Python library: pricing, greeks, positions, strategies, analyzer, plots |
| [`data/samples/`](data/samples/) | Offline sample option chains so every notebook runs without internet |
| [`tests/`](tests/) | Pytest suite — the acceptance criteria for the library |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # library + notebooks + tests
pytest                           # everything should be green
jupyter lab                      # open curriculum/00-foundations/notebook.ipynb
```

Optional live market data (not required anywhere in the curriculum):

```bash
pip install -e ".[live]"         # adds yfinance
```

## How to use this repo

1. Read `ROADMAP.md` first — it is the workflow.
2. Work modules in order (`curriculum/00-…` → `11-…`): read `lesson.md`, run and modify
   `notebook.ipynb`, do `exercises.md`, and only move on when you pass the module's exit gate.
3. From Phase 2 onward, paper-trade what you learn and keep the journal (template in module 10).
4. Track your progress in `TODO.md`.

## Quick taste

```python
from optionslab import strategies, analyzer, viz

# 45-DTE iron condor on a $100 stock: legs given as (strike, premium)
ic = strategies.iron_condor(
    long_put=(85, 0.55), short_put=(90, 1.10),
    short_call=(110, 1.05), long_call=(115, 0.50),
    expiry=45 / 365,
)
print(analyzer.summarize(ic, spot=100, vol=0.25))
viz.plot_payoff(ic)
```

## Disclaimer

This project is **educational material, not financial advice**. Options involve substantial risk
and are not suitable for every investor. Models here (Black-Scholes-Merton, binomial, lognormal
POP estimates) are simplifications of real markets. Paper-trade first; never risk money you
cannot afford to lose.
