import numpy as np
import pytest

from optionslab.payoff import (
    default_spot_grid,
    payoff_at_expiry,
    pnl_at,
    pnl_at_expiry,
    pnl_curve,
)
from optionslab.position import OptionLeg, Position, StockLeg


@pytest.fixture
def long_call_pos():
    # 100C bought for 3.00
    return Position(legs=(OptionLeg("call", 100, 30 / 365, 1, 3.0),), label="LC")


class TestExpiryPayoff:
    def test_long_call(self, long_call_pos):
        assert payoff_at_expiry(long_call_pos, 110) == pytest.approx(1000.0)
        assert payoff_at_expiry(long_call_pos, 95) == 0.0
        assert pnl_at_expiry(long_call_pos, 110) == pytest.approx(700.0)
        assert pnl_at_expiry(long_call_pos, 95) == pytest.approx(-300.0)
        # breakeven at strike + premium
        assert pnl_at_expiry(long_call_pos, 103) == pytest.approx(0.0, abs=1e-9)

    def test_short_put(self):
        pos = Position(legs=(OptionLeg("put", 90, 0.1, -1, 2.0),))
        assert pnl_at_expiry(pos, 95) == pytest.approx(200.0)  # keeps credit
        assert pnl_at_expiry(pos, 80) == pytest.approx(-800.0)  # -1000 + 200

    def test_covered_call(self):
        pos = Position(
            legs=(StockLeg(100, 100.0), OptionLeg("call", 105, 0.1, -1, 2.0))
        )
        # above the strike: stock gain capped at 105, plus credit
        assert pnl_at_expiry(pos, 120) == pytest.approx(700.0)
        assert pnl_at_expiry(pos, 100) == pytest.approx(200.0)
        assert pnl_at_expiry(pos, 90) == pytest.approx(-800.0)


class TestMarkToModel:
    def test_pnl_at_zero_elapsed_zero_at_entry_price(self, long_call_pos):
        # Marked at the same model price it was bought for => P&L ~ 0
        from optionslab.pricing import implied_vol

        entry_vol = implied_vol("call", 3.0, 100, 100, 30 / 365)
        assert pnl_at(long_call_pos, 100, 0.0, entry_vol) == pytest.approx(0.0, abs=1e-6)

    def test_pnl_at_full_elapse_matches_expiry(self, long_call_pos):
        v = pnl_at(long_call_pos, 112, t_elapsed=30 / 365, vol=0.25)
        assert v == pytest.approx(pnl_at_expiry(long_call_pos, 112), abs=1e-9)

    def test_theta_decay_hurts_long_option(self, long_call_pos):
        now = pnl_at(long_call_pos, 100, 0.0, 0.25)
        later = pnl_at(long_call_pos, 100, 15 / 365, 0.25)
        assert later < now

    def test_vol_crush_hurts_long_option(self, long_call_pos):
        high = pnl_at(long_call_pos, 100, 5 / 365, 0.40)
        low = pnl_at(long_call_pos, 100, 5 / 365, 0.20)
        assert low < high


class TestCurvesAndGrids:
    def test_pnl_curve_expiry_shape_and_values(self, long_call_pos):
        spots = np.array([90.0, 103.0, 120.0])
        curve = pnl_curve(long_call_pos, spots)
        assert curve.shape == (3,)
        assert curve[0] == pytest.approx(-300.0)
        assert curve[1] == pytest.approx(0.0, abs=1e-9)
        assert curve[2] == pytest.approx(1700.0)

    def test_pnl_curve_mtm_requires_vol(self, long_call_pos):
        with pytest.raises(ValueError):
            pnl_curve(long_call_pos, [90, 100], t_elapsed=0.01)

    def test_default_spot_grid_spans_strikes(self, long_call_pos):
        grid = default_spot_grid(long_call_pos)
        assert grid.min() <= 100 * 0.6 + 1e-9
        assert grid.max() >= 100 * 1.4 - 1e-9
        assert len(grid) == 201
