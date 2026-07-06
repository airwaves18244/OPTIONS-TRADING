import matplotlib

matplotlib.use("Agg")

import pytest

from optionslab import strategies


@pytest.fixture
def demo_iron_condor():
    """45-DTE iron condor on a $100 underlying; net credit $1.10 per share."""
    return strategies.iron_condor(
        long_put=(85, 0.55),
        short_put=(90, 1.10),
        short_call=(110, 1.05),
        long_call=(115, 0.50),
        expiry=45 / 365,
    )


@pytest.fixture
def demo_bull_call():
    """95/105 bull call spread, $4.00 debit."""
    return strategies.bull_call_spread(
        long_call=(95, 7.00), short_call=(105, 3.00), expiry=30 / 365
    )
