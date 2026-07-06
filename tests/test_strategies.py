import pytest

from optionslab import strategies
from optionslab.payoff import pnl_at_expiry
from optionslab.position import OptionLeg, Position, StockLeg

E = 45 / 365


class TestFactoryBasics:
    def test_long_call_structure(self):
        pos = strategies.long_call((100, 3.0), expiry=E)
        (leg,) = pos.option_legs
        assert leg.kind == "call" and leg.quantity == 1 and leg.premium == 3.0
        assert pos.net_premium() == pytest.approx(300.0)
        assert pos.label

    def test_quantity_scales_structure(self):
        pos = strategies.iron_condor(
            long_put=(85, 0.55), short_put=(90, 1.10),
            short_call=(110, 1.05), long_call=(115, 0.50),
            expiry=E, quantity=3,
        )
        assert pos.net_premium() == pytest.approx(-110.0 * 3)

    def test_custom_from_raw_legs(self):
        pos = strategies.custom(
            OptionLeg("call", 100, E, 1, 2.0), StockLeg(-100, 101.0), label="X"
        )
        assert isinstance(pos, Position) and pos.label == "X" and len(pos.legs) == 2


class TestDirectionSigns:
    def test_covered_call(self):
        pos = strategies.covered_call(100.0, short_call=(105, 2.0), expiry=E)
        assert pos.stock_legs[0].quantity == 100
        assert pos.option_legs[0].quantity == -1

    def test_credit_verticals_are_credits(self):
        bps = strategies.bull_put_spread(short_put=(95, 2.0), long_put=(90, 1.0), expiry=E)
        bcs = strategies.bear_call_spread(short_call=(105, 2.0), long_call=(110, 1.0), expiry=E)
        assert bps.net_premium() < 0
        assert bcs.net_premium() < 0

    def test_debit_verticals_are_debits(self):
        bc = strategies.bull_call_spread(long_call=(95, 7.0), short_call=(105, 3.0), expiry=E)
        bp = strategies.bear_put_spread(long_put=(105, 7.0), short_put=(95, 3.0), expiry=E)
        assert bc.net_premium() > 0
        assert bp.net_premium() > 0


class TestValidation:
    def test_bull_call_strike_order(self):
        with pytest.raises(ValueError):
            strategies.bull_call_spread(long_call=(105, 3.0), short_call=(95, 7.0), expiry=E)

    def test_iron_condor_strike_order(self):
        with pytest.raises(ValueError):
            strategies.iron_condor(
                long_put=(90, 1.0), short_put=(85, 0.5),
                short_call=(110, 1.0), long_call=(115, 0.5), expiry=E,
            )

    def test_straddle_requires_same_strike(self):
        with pytest.raises(ValueError):
            strategies.long_straddle(call=(100, 2.0), put=(95, 2.0), expiry=E)

    def test_strangle_requires_put_below_call(self):
        with pytest.raises(ValueError):
            strategies.short_strangle(put=(110, 1.0), call=(90, 1.0), expiry=E)

    def test_iron_butterfly_requires_shared_body(self):
        with pytest.raises(ValueError):
            strategies.iron_butterfly(
                long_put=(90, 0.5), short_put=(100, 3.0),
                short_call=(101, 3.0), long_call=(110, 0.5), expiry=E,
            )

    def test_calendar_requires_front_before_back(self):
        with pytest.raises(ValueError):
            strategies.calendar_spread(
                "call", 100,
                front_expiry=60 / 365, front_premium=3.0,
                back_expiry=30 / 365, back_premium=2.0,
            )

    def test_ratio_requires_short_heavier(self):
        with pytest.raises(ValueError):
            strategies.call_ratio_spread(
                long_call=(100, 3.0), short_call=(105, 2.0), expiry=E, ratio=(2, 1)
            )

    def test_collar_put_below_call(self):
        with pytest.raises(ValueError):
            strategies.collar(100.0, long_put=(105, 3.0), short_call=(95, 3.0), expiry=E)


class TestPayoffCorrectness:
    def test_iron_condor_payoff_regions(self, demo_iron_condor):
        # inside the body: keep the full credit ($110)
        assert pnl_at_expiry(demo_iron_condor, 100) == pytest.approx(110.0)
        # beyond either wing: max loss = -(width - credit) = -390
        assert pnl_at_expiry(demo_iron_condor, 80) == pytest.approx(-390.0)
        assert pnl_at_expiry(demo_iron_condor, 120) == pytest.approx(-390.0)

    def test_bull_call_payoff(self, demo_bull_call):
        assert pnl_at_expiry(demo_bull_call, 90) == pytest.approx(-400.0)
        assert pnl_at_expiry(demo_bull_call, 110) == pytest.approx(600.0)
        assert pnl_at_expiry(demo_bull_call, 99) == pytest.approx(0.0, abs=1e-9)

    def test_long_call_butterfly(self):
        fly = strategies.long_call_butterfly(
            low=(95, 6.0), mid=(100, 3.0), high=(105, 1.5), expiry=E
        )
        # debit = 6 - 6 + 1.5 = 1.5
        assert fly.net_premium() == pytest.approx(150.0)
        assert pnl_at_expiry(fly, 100) == pytest.approx((5 - 1.5) * 100)
        assert pnl_at_expiry(fly, 80) == pytest.approx(-150.0)
        assert pnl_at_expiry(fly, 120) == pytest.approx(-150.0)

    def test_jade_lizard_no_upside_risk(self):
        jl = strategies.jade_lizard(
            short_put=(95, 2.0), short_call=(105, 1.5), long_call=(110, 0.4), expiry=E
        )
        # credit 3.10 > call spread width 5? No: 3.10 < 5 → upside P&L = credit - width
        assert pnl_at_expiry(jl, 150) == pytest.approx((3.10 - 5.0) * 100)
        assert pnl_at_expiry(jl, 100) == pytest.approx(310.0)

    def test_call_backspread_unlimited_upside(self):
        bs = strategies.call_backspread(
            short_call=(100, 5.0), long_call=(110, 2.0), expiry=E
        )
        # net credit 1.00/share; far upside gains ~ (S-110)*100 net of spread loss
        assert pnl_at_expiry(bs, 200) > pnl_at_expiry(bs, 150) > 0

    def test_pmcc_legs(self):
        p = strategies.poor_mans_covered_call(
            long_call=(70, 32.0), short_call=(110, 1.0),
            long_expiry=365 / 365, short_expiry=30 / 365,
        )
        legs = {(l.kind, l.strike, l.quantity, l.expiry) for l in p.option_legs}
        assert ("call", 70.0, 1, 1.0) in legs
        assert ("call", 110.0, -1, 30 / 365) in legs
