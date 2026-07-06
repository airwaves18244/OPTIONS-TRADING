import numpy as np
import pytest
from matplotlib.axes import Axes

from optionslab import analyzer, data, strategies, viz


class TestSampleData:
    def test_list_names(self):
        names = data.list_sample_chains()
        assert {"DEMO", "LOWVOL", "HIGHVOL"}.issubset(set(names))

    def test_load_demo_schema(self):
        df = data.load_sample_chain("DEMO")
        required = {
            "kind", "strike", "expiry_days", "bid", "ask", "mid", "iv",
            "volume", "open_interest", "spot",
        }
        assert required.issubset(df.columns)
        assert set(df["kind"].unique()) == {"call", "put"}
        assert (df["iv"] > 0).all()
        assert df["spot"].nunique() == 1

    def test_missing_chain_raises_with_names(self):
        with pytest.raises(FileNotFoundError) as ei:
            data.load_sample_chain("NOPE")
        assert "DEMO" in str(ei.value)


class TestViz:
    def test_plot_payoff_returns_axes(self, demo_iron_condor):
        ax = viz.plot_payoff(demo_iron_condor, spot=100, vol=0.25)
        assert isinstance(ax, Axes)
        assert len(ax.lines) >= 2  # expiry line + mtm curve at least

    def test_plot_payoff_expiry_only(self, demo_bull_call):
        ax = viz.plot_payoff(demo_bull_call)
        assert isinstance(ax, Axes)

    def test_plot_greeks(self, demo_iron_condor):
        ax = viz.plot_greeks(demo_iron_condor, vol=0.25)
        assert isinstance(ax, Axes)
        assert len(ax.lines) >= 4

    def test_plot_heatmap(self, demo_iron_condor):
        grid = analyzer.scenario_grid(
            demo_iron_condor, np.linspace(80, 120, 11), days_forward=[0, 20, 45], vol=0.25
        )
        ax = viz.plot_pnl_heatmap(grid)
        assert isinstance(ax, Axes)

    def test_plot_compare(self, demo_iron_condor, demo_bull_call):
        ax = viz.plot_compare([demo_iron_condor, demo_bull_call])
        assert isinstance(ax, Axes)
        assert ax.get_legend() is not None
