import pytest

from optionslab.position import OptionLeg, Position, StockLeg


class TestOptionLegValidation:
    def test_valid_leg(self):
        leg = OptionLeg("put", 90.0, 45 / 365, -1, 1.10)
        assert leg.multiplier == 100

    @pytest.mark.parametrize(
        "kwargs",
        [
            dict(kind="callx", strike=100, expiry=0.1, quantity=1, premium=1.0),
            dict(kind="call", strike=0, expiry=0.1, quantity=1, premium=1.0),
            dict(kind="call", strike=100, expiry=0.0, quantity=1, premium=1.0),
            dict(kind="call", strike=100, expiry=0.1, quantity=0, premium=1.0),
            dict(kind="call", strike=100, expiry=0.1, quantity=1, premium=-0.5),
        ],
    )
    def test_invalid_leg_raises(self, kwargs):
        with pytest.raises(ValueError):
            OptionLeg(**kwargs)

    def test_entry_cash_flow_sign(self):
        long = OptionLeg("call", 100, 0.1, 2, 3.0)
        short = OptionLeg("call", 100, 0.1, -2, 3.0)
        assert long.entry_cash_flow == pytest.approx(600.0)  # debit
        assert short.entry_cash_flow == pytest.approx(-600.0)  # credit

    def test_intrinsic(self):
        call = OptionLeg("call", 100, 0.1, 1, 1.0)
        put = OptionLeg("put", 100, 0.1, 1, 1.0)
        assert call.intrinsic(110) == pytest.approx(10.0)
        assert call.intrinsic(90) == 0.0
        assert put.intrinsic(90) == pytest.approx(10.0)
        assert put.intrinsic(110) == 0.0


class TestStockLeg:
    def test_cash_flow(self):
        assert StockLeg(100, 50.0).entry_cash_flow == pytest.approx(5000.0)
        assert StockLeg(-100, 50.0).entry_cash_flow == pytest.approx(-5000.0)

    def test_invalid(self):
        with pytest.raises(ValueError):
            StockLeg(0, 50.0)
        with pytest.raises(ValueError):
            StockLeg(100, 0.0)


class TestPosition:
    def test_net_premium_credit_structure(self):
        pos = Position(
            legs=(
                OptionLeg("put", 90, 45 / 365, -1, 1.10),
                OptionLeg("put", 85, 45 / 365, 1, 0.55),
            )
        )
        # short 1.10, long 0.55 => net credit 0.55/share = -$55
        assert pos.net_premium() == pytest.approx(-55.0)

    def test_empty_position_raises(self):
        with pytest.raises(ValueError):
            Position(legs=())

    def test_legs_normalized_to_tuple_and_iterable(self):
        legs = [OptionLeg("call", 100, 0.1, 1, 1.0), StockLeg(100, 99.0)]
        pos = Position(legs=legs)  # list accepted
        assert isinstance(pos.legs, tuple)
        assert len(list(pos)) == 2
        assert len(pos.option_legs) == 1
        assert len(pos.stock_legs) == 1

    def test_earliest_expiry(self):
        pos = Position(
            legs=(
                OptionLeg("call", 100, 30 / 365, -1, 1.0),
                OptionLeg("call", 100, 60 / 365, 1, 2.0),
            )
        )
        assert pos.earliest_expiry == pytest.approx(30 / 365)

    def test_earliest_expiry_no_options_raises(self):
        with pytest.raises(ValueError):
            _ = Position(legs=(StockLeg(100, 50.0),)).earliest_expiry

    def test_describe_mentions_label_and_legs(self):
        pos = Position(legs=(OptionLeg("call", 100, 0.1, 1, 1.0),), label="Test Call")
        text = pos.describe()
        assert "Test Call" in text
        assert "100" in text
