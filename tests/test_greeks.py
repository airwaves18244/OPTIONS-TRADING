import pytest

from optionslab.greeks import Greeks, bsm_greeks, numeric_greeks, position_greeks
from optionslab.position import OptionLeg, Position, StockLeg


class TestGreeksContainer:
    def test_add_and_scale(self):
        a = Greeks(0.5, 0.02, -0.01, 0.10, 0.05)
        b = Greeks(-0.3, 0.01, -0.02, 0.05, 0.01)
        s = a + b
        assert s.delta == pytest.approx(0.2)
        assert s.theta == pytest.approx(-0.03)
        doubled = 2 * a
        assert doubled.vega == pytest.approx(0.20)
        assert (a * -1).delta == pytest.approx(-0.5)


class TestBsmGreeksReference:
    # S=100, K=100, t=1, vol=0.2, r=0.05 — precomputed analytic values
    def test_call_greeks(self):
        g = bsm_greeks("call", 100, 100, 1.0, 0.2, rate=0.05)
        assert g.delta == pytest.approx(0.636831, abs=1e-4)
        assert g.gamma == pytest.approx(0.018762, abs=1e-5)
        assert g.theta == pytest.approx(-0.0175727, abs=1e-5)  # per calendar day
        assert g.vega == pytest.approx(0.375240, abs=1e-4)  # per 1 vol point
        assert g.rho == pytest.approx(0.532325, abs=1e-4)  # per 1% rate

    def test_put_delta_via_parity(self):
        c = bsm_greeks("call", 100, 100, 1.0, 0.2, rate=0.05)
        p = bsm_greeks("put", 100, 100, 1.0, 0.2, rate=0.05)
        assert p.delta == pytest.approx(c.delta - 1.0, abs=1e-9)
        assert p.gamma == pytest.approx(c.gamma, abs=1e-9)
        assert p.vega == pytest.approx(c.vega, abs=1e-9)

    def test_expired_greeks_are_intrinsic_limits(self):
        g = bsm_greeks("call", 120, 100, 0.0, 0.2)
        assert g.delta == pytest.approx(1.0)
        assert g.gamma == 0 and g.vega == 0 and g.theta == 0


class TestNumericAgreesWithAnalytic:
    @pytest.mark.parametrize("kind", ["call", "put"])
    @pytest.mark.parametrize("spot", [85.0, 100.0, 118.0])
    def test_agreement(self, kind, spot):
        a = bsm_greeks(kind, spot, 100, 0.5, 0.3, rate=0.02, div_yield=0.01)
        n = numeric_greeks(kind, spot, 100, 0.5, 0.3, rate=0.02, div_yield=0.01)
        assert n.delta == pytest.approx(a.delta, abs=2e-3)
        assert n.gamma == pytest.approx(a.gamma, abs=2e-3)
        assert n.theta == pytest.approx(a.theta, abs=2e-3)
        assert n.vega == pytest.approx(a.vega, abs=2e-3)
        assert n.rho == pytest.approx(a.rho, abs=2e-3)


class TestPositionGreeks:
    def test_single_long_call_scales_by_contract(self):
        leg = OptionLeg("call", 100, 0.5, 1, 5.0)
        pos = Position(legs=(leg,))
        pg = position_greeks(pos, spot=100, vol=0.2)
        per_share = bsm_greeks("call", 100, 100, 0.5, 0.2)
        assert pg.delta == pytest.approx(per_share.delta * 100, rel=1e-9)

    def test_short_flips_sign(self):
        pos = Position(legs=(OptionLeg("call", 100, 0.5, -2, 5.0),))
        pg = position_greeks(pos, spot=100, vol=0.2)
        assert pg.delta < 0
        assert pg.theta > 0  # short options collect theta

    def test_stock_leg_is_pure_delta(self):
        pos = Position(legs=(StockLeg(quantity=150, entry_price=95.0),))
        pg = position_greeks(pos, spot=100, vol=0.2)
        assert pg.delta == pytest.approx(150)
        assert pg.gamma == 0 and pg.vega == 0 and pg.theta == 0

    def test_t_elapsed_reduces_time(self):
        pos = Position(legs=(OptionLeg("call", 100, 45 / 365, 1, 2.5),))
        g0 = position_greeks(pos, spot=100, vol=0.25)
        g30 = position_greeks(pos, spot=100, vol=0.25, t_elapsed=30 / 365)
        # ATM gamma grows as expiry approaches
        assert g30.gamma > g0.gamma

    def test_straddle_is_near_delta_neutral(self):
        pos = Position(
            legs=(
                OptionLeg("call", 100, 45 / 365, 1, 2.5),
                OptionLeg("put", 100, 45 / 365, 1, 2.4),
            )
        )
        pg = position_greeks(pos, spot=100, vol=0.25)
        assert abs(pg.delta) < 15  # ~100-share tolerance band around neutral
        assert pg.vega > 0
