"""W3 策略层单元测试"""
import pytest
import sys
from pathlib import Path
import pandas as pd

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.strategies import TurtleStrategy, ChanlunStrategy, MultiFactorStrategy
from htzl_a_share_mcp.data_sources import MockDataSource


class TestTurtleStrategy:
    """海龟交易法测试"""

    def setup_method(self):
        self.turtle = TurtleStrategy(n_entry=20, n_exit=10)
        self.df = MockDataSource(base_price=100.0).get_daily("600519", "2025-01-01", "2025-03-31")

    def test_calculate_signals_returns_columns(self):
        df_sig = self.turtle.calculate_signals(self.df)
        assert "N" in df_sig.columns
        assert "entry_high" in df_sig.columns
        assert "entry_low" in df_sig.columns
        assert "buy_signal" in df_sig.columns
        assert "sell_signal" in df_sig.columns
        assert "stop_loss" in df_sig.columns

    def test_calculate_signals_consistent_length(self):
        df_sig = self.turtle.calculate_signals(self.df)
        assert len(df_sig) == len(self.df)

    def test_calculate_position_size_minimum(self):
        """头寸规模最小 100 股（A 股 1 手 = 100 股）"""
        pos = self.turtle.calculate_position_size(100000, 5.0, 50.0)
        assert pos >= 100
        assert pos == int(pos)

    def test_calculate_position_size_zero_N(self):
        """N=0 时返回最小头寸"""
        pos = self.turtle.calculate_position_size(100000, 0.0, 50.0)
        assert pos == 100

    def test_buy_sell_signals_are_boolean(self):
        df_sig = self.turtle.calculate_signals(self.df)
        assert df_sig["buy_signal"].dtype == bool
        assert df_sig["sell_signal"].dtype == bool

    def test_N_is_positive(self):
        """N（波动率）必须为正"""
        df_sig = self.turtle.calculate_signals(self.df)
        assert (df_sig["N"].dropna() > 0).all()


class TestChanlunStrategy:
    """缠论核心测试"""

    def setup_method(self):
        self.chanlun = ChanlunStrategy()
        self.df = MockDataSource(base_price=100.0).get_daily("600519", "2025-01-01", "2025-02-28")
        self.df = self.df.rename(columns={"date": "date"})

    def test_identify_fractals_returns_list(self):
        fractals = self.chanlun.identify_fractals(self.df)
        assert isinstance(fractals, list)
        # 至少能识别出几个分型
        for f in fractals:
            assert f.fractal_type in ('top', 'bottom')
            assert hasattr(f, 'price')
            assert hasattr(f, 'date')

    def test_identify_strokes_alternating(self):
        """笔必须是顶底交替"""
        fractals = self.chanlun.identify_fractals(self.df)
        strokes = self.chanlun.identify_strokes(fractals)
        # 至少保证生成的笔都是交替的（实现只生成交替的笔）
        for i, stroke in enumerate(strokes):
            assert stroke[0].fractal_type != stroke[1].fractal_type, f"笔 {i} 内部不交替"

    def test_strokes_have_direction(self):
        fractals = self.chanlun.identify_fractals(self.df)
        strokes = self.chanlun.identify_strokes(fractals)
        for stroke in strokes:
            assert stroke[2] in ('up', 'down')


class TestMultiFactorStrategy:
    """多因子选股测试"""

    def setup_method(self):
        self.mf = MultiFactorStrategy()
        # 构造 10 只股票的因子数据
        self.df = pd.DataFrame({
            'symbol': [f'stock_{i}' for i in range(10)],
            'pe': [10 + i for i in range(10)],
            'revenue_growth': [0.1 + i * 0.05 for i in range(10)],
            'roe': [0.05 + i * 0.02 for i in range(10)],
            'return_20d': [0.01 * (i - 5) for i in range(10)],
        })

    def test_calculate_factor_score_value(self):
        scores = self.mf.calculate_factor_score(self.df, "value")
        assert all(-0.01 <= s <= 1.01 for s in scores)
        # 低 PE 应该是高分
        assert scores.iloc[0] > scores.iloc[-1]

    def test_calculate_factor_score_growth(self):
        scores = self.mf.calculate_factor_score(self.df, "growth")
        assert all(0 <= s <= 1 for s in scores)

    def test_calculate_factor_score_unknown(self):
        """未知因子返回 0.5 中性"""
        scores = self.mf.calculate_factor_score(self.df, "unknown_factor")
        assert all(s == 0.5 for s in scores)

    def test_select_stocks_top_n(self):
        selected = self.mf.select_stocks(self.df, top_n=3)
        assert len(selected) == 3
        assert 'rank' in selected.columns
        assert 'composite_score' in selected.columns
        # 第一名应该是高分股票
        assert selected.iloc[0]['composite_score'] >= selected.iloc[-1]['composite_score']

    def test_select_stocks_invalid_factor_does_not_crash(self):
        """无效因子不应该导致崩溃"""
        df_bad = self.df.copy()
        df_bad['pe'] = None
        selected = self.mf.select_stocks(df_bad, top_n=5)
        assert len(selected) == 5