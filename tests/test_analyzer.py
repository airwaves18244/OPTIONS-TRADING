import math

import numpy as np
import pytest

from optionslab import analyzer, strategies
from optionslab.greeks import Greeks

E = 45 / 365


class TestBreakevens:
    def test_iron_condor_two_breakevens(self, demo_iron_condor):
        bes = analyzer.breakevens(demo_iron_condor)
        assert len(bes) == 2
        assert bes[0] == pytest.approx(88.90, abs=0.01)
        assert bes[1] == pytest.approx(111.10, abs=0.01)

    def test_bull_call_single_breakeven(self, demo_bull_call):
        bes = analyzer.breakevens(demo_bull_call)
        assert len(bes) == 1
        assert bes[0] == pytest.approx(99.0, abs=0.01)

    def test_sorted_ascending(self, demo_iron_condor):
        bes = analyzer.breakevens(demo_iron_condor)
        assert bes == sorted(bes)


class TestMaxProfitLoss:
    def test_iron_condor_bounded(self, demo_iron_condor):
        assert analyzer.max_profit(demo_iron_condor) == pytest.approx(110.0, abs=0.5)
        assert analyzer.max_loss(demo_iron_condor) == pytest.approx(-390.0, abs=0.5)

    def test_long_call_unbounded_profit(self):
        lc = strategies.long_call((100, 3.0), expiry=E)
        assert analyzer.max_profit(lc) == math.inf
        assert analyzer.max_loss(lc) == pytest.approx(-300.0, abs=0.5)

    def test_short_call_unbounded_loss(self):
        sc = strategies.short_call((100, 3.0), expiry=E)
        assert analyzer.max_profit(sc) == pytest.approx(300.0, abs=0.5)
        assert analyzer.max_loss(sc) == -math.inf

    def test_short_put_loss_bounded_by_zero(self):
        sp = strategies.short_put((90, 2.0), expiry=E)
        # worst case at S=0: -(90*100) + 200
        assert analyzer.max_loss(sp) == pytest.approx(-8800.0, abs=1.0)
        assert analyzer.max_loss(sp) != -math.inf


class TestExpectedMoveAndPop:
    def test_expected_move(self):
        assert analyzer.expected_move(100, 0.25, 45 / 365) == pytest.approx(
            100 * 0.25 * math.sqrt(45 / 365), rel=1e-9
        )

    def test_pop_in_unit_interval(self, demo_iron_condor):
        pop = analyzer.probability_of_profit(demo_iron_condor, spot=100, vol=0.25)
        assert 0.0 < pop < 1.0

    def test_iron_condor_pop_reasonable(self, demo_iron_condor):
        # Breakevens ±11% away, 45 DTE @ 25% vol (~8.8% 1-sigma): POP well above half
        pop = analyzer.probability_of_profit(demo_iron_condor, spot=100, vol=0.25)
        assert 0.6 < pop < 0.95

    def test_pop_falls_when_vol_rises_for_short_premium(self, demo_iron_condor):
        low = analyzer.probability_of_profit(demo_iron_condor, spot=100, vol=0.15)
        high = analyzer.probability_of_profit(demo_iron_condor, spot=100, vol=0.45)
        assert high < low

    def test_deep_itm_call_pop_near_one(self):
        lc = strategies.long_call((50, 0.10), expiry=E)  # basically free deep ITM
        pop = analyzer.probability_of_profit(lc, spot=100, vol=0.2)
        assert pop > 0.95


class TestScenarioGrid:
    def test_shape_and_columns(self, demo_iron_condor):
        spots = np.linspace(80, 120, 9)
        grid = analyzer.scenario_grid(
            demo_iron_condor, spots, days_forward=[0, 15, 30, 45], vol=0.25
        )
        assert set(["spot", "days_forward", "vol", "pnl"]).issubset(grid.columns)
        assert len(grid) == 9 * 4

    def test_vol_shift_axis(self, demo_iron_condor):
        grid = analyzer.scenario_grid(
            demo_iron_condor, [100.0], days_forward=[10], vol=0.25,
            vol_shift=[-0.05, 0.0, 0.05],
        )
        assert len(grid) == 3
        assert set(np.round(grid["vol"], 4)) == {0.20, 0.25, 0.30}

    def test_terminal_day_matches_expiry_pnl(self, demo_iron_condor):
        from optionslab.payoff import pnl_at_expiry

        grid = analyzer.scenario_grid(
            demo_iron_condor, [100.0], days_forward=[45], vol=0.25
        )
        assert grid["pnl"].iloc[0] == pytest.approx(pnl_at_expiry(demo_iron_condor, 100.0), abs=1e-6)

    def test_negative_days_raise(self, demo_iron_condor):
        with pytest.raises(ValueError):
            analyzer.scenario_grid(demo_iron_condor, [100.0], days_forward=[-1], vol=0.25)


class TestSummarize:
    def test_keys_and_consistency(self, demo_iron_condor):
        s = analyzer.summarize(demo_iron_condor, spot=100, vol=0.25)
        for key in (
            "label", "net_premium", "breakevens", "max_profit", "max_loss",
            "probability_of_profit", "expected_move", "greeks", "days_to_expiry",
        ):
            assert key in s, key
        assert s["net_premium"] == pytest.approx(-110.0)
        assert s["max_profit"] == pytest.approx(110.0, abs=0.5)
        assert isinstance(s["greeks"], Greeks)
        assert s["days_to_expiry"] == pytest.approx(45, abs=0.51)
        # short premium structure at entry: positive theta, negative vega
        assert s["greeks"].theta > 0
        assert s["greeks"].vega < 0
