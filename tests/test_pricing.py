import math

import pytest

from optionslab.pricing import binomial_price, bsm_price, implied_vol


class TestBsmReferenceValues:
    def test_atm_call_hull_style(self):
        # S=100, K=100, t=1y, vol=20%, r=5%: classic textbook value
        assert bsm_price("call", 100, 100, 1.0, 0.2, rate=0.05) == pytest.approx(
            10.450584, abs=1e-4
        )

    def test_atm_put_hull_style(self):
        assert bsm_price("put", 100, 100, 1.0, 0.2, rate=0.05) == pytest.approx(
            5.573526, abs=1e-4
        )

    def test_zero_rate_atm_call_equals_put(self):
        c = bsm_price("call", 100, 100, 0.25, 0.2)
        p = bsm_price("put", 100, 100, 0.25, 0.2)
        assert c == pytest.approx(3.987761, abs=1e-4)
        assert c == pytest.approx(p, abs=1e-10)

    def test_with_dividend_yield(self):
        assert bsm_price("call", 100, 95, 0.5, 0.3, rate=0.03, div_yield=0.02) == pytest.approx(
            11.127317, abs=1e-4
        )
        assert bsm_price("put", 100, 95, 0.5, 0.3, rate=0.03, div_yield=0.02) == pytest.approx(
            5.707968, abs=1e-4
        )


class TestPutCallParity:
    @pytest.mark.parametrize("spot", [80.0, 100.0, 123.4])
    @pytest.mark.parametrize("t,vol,r,q", [(0.5, 0.25, 0.04, 0.0), (1.5, 0.4, 0.02, 0.01)])
    def test_parity(self, spot, t, vol, r, q):
        K = 100.0
        c = bsm_price("call", spot, K, t, vol, rate=r, div_yield=q)
        p = bsm_price("put", spot, K, t, vol, rate=r, div_yield=q)
        lhs = c - p
        rhs = spot * math.exp(-q * t) - K * math.exp(-r * t)
        assert lhs == pytest.approx(rhs, abs=1e-8)


class TestEdgeCases:
    def test_expired_returns_intrinsic(self):
        assert bsm_price("call", 105, 100, 0.0, 0.2) == pytest.approx(5.0)
        assert bsm_price("put", 105, 100, 0.0, 0.2) == pytest.approx(0.0)
        assert bsm_price("put", 90, 100, -0.01, 0.2) == pytest.approx(10.0)

    def test_zero_vol_returns_intrinsic(self):
        assert bsm_price("call", 120, 100, 0.5, 0.0) == pytest.approx(20.0, abs=1e-6)

    def test_invalid_kind_raises(self):
        with pytest.raises(ValueError):
            bsm_price("CALL-ish", 100, 100, 1.0, 0.2)

    def test_nonpositive_spot_or_strike_raises(self):
        with pytest.raises(ValueError):
            bsm_price("call", 0.0, 100, 1.0, 0.2)
        with pytest.raises(ValueError):
            bsm_price("call", 100, -5, 1.0, 0.2)

    def test_deep_itm_call_near_forward_intrinsic(self):
        # Deep ITM, tiny vol: value ~ S - K e^{-rt}
        v = bsm_price("call", 200, 100, 0.5, 0.01, rate=0.03)
        assert v == pytest.approx(200 - 100 * math.exp(-0.03 * 0.5), abs=1e-3)


class TestBinomial:
    def test_european_converges_to_bsm(self):
        bs = bsm_price("call", 100, 100, 1.0, 0.2, rate=0.05)
        tree = binomial_price("call", 100, 100, 1.0, 0.2, rate=0.05, steps=400, american=False)
        assert tree == pytest.approx(bs, abs=0.02)

    def test_american_put_worth_more_than_european(self):
        eur = binomial_price("put", 90, 100, 1.0, 0.2, rate=0.06, steps=300, american=False)
        amr = binomial_price("put", 90, 100, 1.0, 0.2, rate=0.06, steps=300, american=True)
        assert amr > eur + 1e-4

    def test_american_call_no_dividend_equals_european(self):
        # Never optimal to exercise an American call early without dividends
        eur = binomial_price("call", 110, 100, 1.0, 0.25, rate=0.05, steps=300, american=False)
        amr = binomial_price("call", 110, 100, 1.0, 0.25, rate=0.05, steps=300, american=True)
        assert amr == pytest.approx(eur, abs=1e-6)

    def test_bad_steps_raises(self):
        with pytest.raises(ValueError):
            binomial_price("call", 100, 100, 1.0, 0.2, steps=0)


class TestImpliedVol:
    @pytest.mark.parametrize("kind", ["call", "put"])
    @pytest.mark.parametrize("vol", [0.1, 0.25, 0.8])
    def test_round_trip(self, kind, vol):
        price = bsm_price(kind, 100, 105, 0.4, vol, rate=0.03)
        assert implied_vol(kind, price, 100, 105, 0.4, rate=0.03) == pytest.approx(
            vol, abs=1e-5
        )

    def test_price_below_intrinsic_raises(self):
        with pytest.raises(ValueError):
            implied_vol("call", 4.0, 110, 100, 0.5)  # intrinsic is 10

    def test_expired_raises(self):
        with pytest.raises(ValueError):
            implied_vol("call", 5.0, 105, 100, 0.0)
