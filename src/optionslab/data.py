"""Option-chain data: bundled offline samples, plus optional live fetch via yfinance.

Sample chains live in ``data/samples/*.csv`` at the repository root with columns:
``kind`` ("call"/"put"), ``strike``, ``expiry_days`` (int), ``bid``, ``ask``, ``mid``,
``iv`` (decimal), ``volume``, ``open_interest``, ``spot`` (repeated on every row).

The curriculum only relies on the offline samples; ``fetch_chain`` exists so the
same code paths work with live data when available (SPEC v2 hardens this).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SAMPLES_DIR = Path(__file__).resolve().parents[2] / "data" / "samples"


def list_sample_chains() -> list[str]:
    """Names (file stems) of available sample chains, sorted."""
    raise NotImplementedError


def load_sample_chain(name: str = "DEMO") -> pd.DataFrame:
    """Load ``data/samples/<name>.csv`` with the documented column schema.

    Raises ``FileNotFoundError`` with the list of available names when missing.
    Validates required columns are present.
    """
    raise NotImplementedError


def fetch_chain(ticker: str, expiry: str | None = None) -> pd.DataFrame:
    """Live option chain via ``yfinance``, normalized to the sample-chain schema.

    ``expiry`` is a ``YYYY-MM-DD`` string; None picks the nearest listed expiry.
    Raises ``ImportError`` with install instructions if yfinance is not installed;
    network errors propagate. ``iv`` falls back to NaN when the source omits it.
    """
    raise NotImplementedError
