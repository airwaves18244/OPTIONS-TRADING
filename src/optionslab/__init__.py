"""optionslab — educational options strategy construction and analysis.

Conventions used across the whole package (see SPEC.md):

- Time to expiry ``t`` is in **years** (45 DTE == ``45/365``); ``t = 0`` means at expiry.
- Volatility is annualized, decimal (``0.25`` == 25%). Rates and dividend yields likewise.
- ``quantity`` sign carries direction: positive = long, negative = short.
- Option premiums are entry prices **per share**, always >= 0.
- Position-level P&L, premiums, and greeks are in **dollars**, aggregated over
  ``quantity * multiplier``.
- ``theta`` is per calendar day, ``vega`` per 1 vol point (+0.01 IV), ``rho`` per +1% rate.
"""

from optionslab import analyzer, data, greeks, payoff, position, pricing, strategies, viz
from optionslab.greeks import Greeks, bsm_greeks, numeric_greeks, position_greeks
from optionslab.payoff import payoff_at_expiry, pnl_at, pnl_at_expiry, pnl_curve
from optionslab.position import OptionLeg, Position, StockLeg
from optionslab.pricing import binomial_price, bsm_price, implied_vol

__version__ = "0.1.0"

__all__ = [
    "analyzer",
    "data",
    "greeks",
    "payoff",
    "position",
    "pricing",
    "strategies",
    "viz",
    "Greeks",
    "OptionLeg",
    "Position",
    "StockLeg",
    "bsm_greeks",
    "numeric_greeks",
    "position_greeks",
    "payoff_at_expiry",
    "pnl_at",
    "pnl_at_expiry",
    "pnl_curve",
    "binomial_price",
    "bsm_price",
    "implied_vol",
]
