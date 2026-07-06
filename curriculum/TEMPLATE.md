# Curriculum authoring template & style guide

Every module directory contains exactly three files: `lesson.md`, `notebook.ipynb`, `exercises.md`.

## `lesson.md`

Structure (strategy modules follow this order; concept modules 00–02 and 08–10 adapt sensibly):

1. **Title + one-paragraph "why this module"** — what you can do after it that you couldn't before.
2. **Concepts / Mechanics** — the theory, precise but plain-spoken. Define every term at first use.
3. For each strategy covered, the **strategy card** template:
   - Construction (legs) and net debit/credit
   - Payoff shape & greeks profile (what you're long/short: direction, vol, time)
   - **When to use it**: market view + IV environment (high/low IV rank) + horizon
   - Entry criteria (strike selection logic, DTE, liquidity)
   - Management & adjustment rules (profit target, loss trigger, what to do when tested)
   - Exit rules
   - Common mistakes
4. **Key takeaways** — 5–8 bullet summary.
5. **In the next module** — one line.

Tone: direct, practical, senior-mentor voice. Concrete numbers over abstractions
(use the $100 DEMO underlying for examples). US equity options context. No hype,
no "guaranteed income" language; always name the risk that pays the reward.

## `notebook.ipynb`

- First cell: markdown title + what the lab will demonstrate.
- Second cell: imports —
  `import numpy as np`, `import matplotlib.pyplot as plt`,
  `from optionslab import pricing, greeks, strategies, analyzer, payoff, viz, data`
  (subset as needed).
- Alternate short markdown explanation cells with code cells. Every code cell ≤ ~15 lines.
- Use ONLY the public API documented in the `src/optionslab/*.py` docstrings and SPEC.md.
- Chain data comes from `data.load_sample_chain("DEMO"|"LOWVOL"|"HIGHVOL")` — never the network.
- End with an **"Experiments"** markdown cell: 3–5 prompts telling the learner what to change
  and re-run ("Move the short strike to the 30-delta and re-run — what happened to POP?").
- Notebooks must be valid `nbformat` v4 JSON, kernel `python3`, and must run top-to-bottom
  offline once `optionslab` is implemented. Do not pre-fill outputs.

## `exercises.md`

- 6–10 exercises: mix of calculation (verifiable with the library), scenario judgment
  ("IV rank 8, you're moderately bullish, 60 days — pick a structure and defend it"),
  and one "break it" exercise (find the flaw in a described trade).
- **Answer key** at the bottom under a `---` rule, with reasoning, not bare answers.
