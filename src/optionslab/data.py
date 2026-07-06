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


_REQUIRED_COLUMNS = {
    "kind",
    "strike",
    "expiry_days",
    "bid",
    "ask",
    "mid",
    "iv",
    "volume",
    "open_interest",
    "spot",
}


def list_sample_chains() -> list[str]:
    """Names (file stems) of available sample chains, sorted."""
    return sorted(p.stem for p in SAMPLES_DIR.glob("*.csv"))


def load_sample_chain(name: str = "DEMO") -> pd.DataFrame:
    """Load ``data/samples/<name>.csv`` with the documented column schema.

    Raises ``FileNotFoundError`` with the list of available names when missing.
    Validates required columns are present.
    """
    path = SAMPLES_DIR / f"{name}.csv"
    if not path.exists():
        available = list_sample_chains()
        raise FileNotFoundError(
            f"sample chain {name!r} not found; available chains: {available}"
        )
    df = pd.read_csv(path)
    missing = _REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"sample chain {name!r} missing required columns: {sorted(missing)}")
    return df


def fetch_chain(ticker: str, expiry: str | None = None) -> pd.DataFrame:
    """Live option chain via ``yfinance``, normalized to the sample-chain schema.

    ``expiry`` is a ``YYYY-MM-DD`` string; None picks the nearest listed expiry.
    Raises ``ImportError`` with install instructions if yfinance is not installed;
    network errors propagate. ``iv`` falls back to NaN when the source omits it.
    """
    try:
        import yfinance as yf
    except ImportError as exc:  # pragma: no cover - exercised only without yfinance
        raise ImportError(
            "fetch_chain requires the optional 'yfinance' package. "
            "Install it with `pip install yfinance`."
        ) from exc

    tk = yf.Ticker(ticker)
    expiries = tk.options
    if not expiries:
        raise ValueError(f"no listed option expiries for {ticker!r}")
    chosen = expiry if expiry is not None else expiries[0]
    chain = tk.option_chain(chosen)

    try:
        spot = tk.fast_info["last_price"]
    except Exception:  # pragma: no cover - network dependent
        spot = float("nan")

    from datetime import date

    exp_date = date.fromisoformat(chosen)
    expiry_days = (exp_date - date.today()).days

    frames = []
    for kind, df in (("call", chain.calls), ("put", chain.puts)):
        out = pd.DataFrame()
        out["kind"] = [kind] * len(df)
        out["strike"] = df["strike"].to_numpy()
        out["expiry_days"] = expiry_days
        out["bid"] = df["bid"].to_numpy()
        out["ask"] = df["ask"].to_numpy()
        out["mid"] = (df["bid"].to_numpy() + df["ask"].to_numpy()) / 2.0
        out["iv"] = df["impliedVolatility"].to_numpy() if "impliedVolatility" in df else float("nan")
        out["volume"] = df["volume"].to_numpy() if "volume" in df else float("nan")
        out["open_interest"] = df["openInterest"].to_numpy() if "openInterest" in df else float("nan")
        out["spot"] = spot
        frames.append(out)

    return pd.concat(frames, ignore_index=True)
