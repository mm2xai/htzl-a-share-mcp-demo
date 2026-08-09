"""W6 29 Skills 完整测试"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.skills import (
    # 数据层
    get_stock_daily, get_stock_realtime, get_stock_basic, get_etf_list, get_index_daily,
    # 资金流向
    get_capital_flow, get_sector_flow,
    # 涨停追踪
    get_limit_up_pool, get_limit_up_stats,
    # 技术面
    turtle_signal, macd_signal, kdj_signal,
    # 估值
    get_pe, get_pb,
    # 财报
    get_income_statement, get_financial_indicators,
    # 多因子
    multi_factor_select,
    # 回测
    backtest_turtle, backtest_multi_factor, backtest_compare,
    # 风控
    risk_var, risk_position_size,
    # 智能报告
    generate_daily_report, generate_sector_report, generate_portfolio_report,
    # 自选股监控
    add_to_watchlist, get_watchlist_alerts,
    # 雪球调仓
    get_xueqiu_quote, track_xueqiu_portfolio,
    # 注册表
    ALL_SKILLS, get_all_skill_names,
)


class TestSkillsRegistry:
    """Skills 注册表测试"""

    def test_all_skills_count(self):
        """必须正好 29 个 skills"""
        names = get_all_skill_names()
        assert len(names) == 29, f"应有 29 个，实际 {len(names)}: {names}"

    def test_all_skills_callable(self):
        """所有 skills 都是 callable"""
        for skill in ALL_SKILLS:
            assert callable(skill), f"{skill.__name__} 不可调用"

    def test_all_skill_names_unique(self):
        names = get_all_skill_names()
        assert len(names) == len(set(names)), "有重名"


class TestDataSkills:
    """数据层 5 skills"""

    def test_get_stock_daily(self):
        result = get_stock_daily("600519", "2025-01-01", "2025-01-31")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_stock_realtime(self):
        result = get_stock_realtime("600519")
        assert isinstance(result, dict)
        assert result['symbol'] == '600519'

    def test_get_stock_basic(self):
        result = get_stock_basic("600519")
        assert result['pe'] > 0
        assert result['pb'] > 0

    def test_get_etf_list(self):
        result = get_etf_list()
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_get_index_daily(self):
        result = get_index_daily("000300", "2025-01-01", "2025-01-31")
        assert isinstance(result, list)


class TestCapitalFlowSkills:
    """资金流向 2 skills"""

    def test_get_capital_flow(self):
        result = get_capital_flow("600519")
        assert "main_net" in result

    def test_get_sector_flow(self):
        result = get_sector_flow("新能源")
        assert isinstance(result, list)


class TestLimitUpSkills:
    """涨停追踪 2 skills"""

    def test_get_limit_up_pool(self):
        result = get_limit_up_pool()
        assert isinstance(result, list)

    def test_get_limit_up_stats(self):
        result = get_limit_up_stats(days=30)
        assert "burst_rate" in result
        assert "promotion_rate" in result


class TestTechnicalSkills:
    """技术面 3 skills"""

    def test_turtle_signal(self):
        result = turtle_signal("600519")
        assert "buy_signal" in result
        assert "sell_signal" in result
        assert "N" in result

    def test_macd_signal(self):
        result = macd_signal("600519")
        assert "signal" in result

    def test_kdj_signal(self):
        result = kdj_signal("600519")
        assert "signal" in result


class TestValuationSkills:
    """估值 2 skills"""

    def test_get_pe(self):
        result = get_pe("600519")
        assert "pe_ttm" in result

    def test_get_pb(self):
        result = get_pb("600519")
        assert "pb" in result


class TestFinancialSkills:
    """财报 2 skills"""

    def test_get_income_statement(self):
        result = get_income_statement("600519")
        assert "revenue" in result
        assert "net_profit" in result

    def test_get_financial_indicators(self):
        result = get_financial_indicators("600519")
        assert "roe" in result


class TestMultiFactorSkill:
    """多因子 1 skill"""

    def test_multi_factor_select(self):
        result = multi_factor_select(top_n=5)
        assert isinstance(result, list)
        assert len(result) == 5


class TestBacktestSkills:
    """回测 3 skills"""

    def test_backtest_turtle(self):
        result = backtest_turtle("600519", "2025-01-01", "2025-12-31")
        assert "sharpe" in result
        assert "max_drawdown" in result

    def test_backtest_multi_factor(self):
        result = backtest_multi_factor("2025-01-01", "2025-12-31")
        assert "annual_return" in result

    def test_backtest_compare(self):
        result = backtest_compare(["turtle", "multi_factor"], "2025-01-01", "2025-12-31")
        assert "result" in result


class TestRiskSkills:
    """风控 2 skills"""

    def test_risk_var(self):
        result = risk_var("600519")
        assert "var" in result
        assert result["var"] < 0  # VaR 是负值

    def test_risk_position_size(self):
        result = risk_position_size(100000, 0.01, 0.05)
        assert result["position"] > 0


class TestReportSkills:
    """智能报告 3 skills"""

    def test_generate_daily_report(self):
        result = generate_daily_report("600519")
        assert "action" in result

    def test_generate_sector_report(self):
        result = generate_sector_report("新能源")
        assert "leaders" in result

    def test_generate_portfolio_report(self):
        result = generate_portfolio_report()
        assert "total_value" in result


class TestWatchlistSkills:
    """自选股监控 2 skills"""

    def test_add_to_watchlist(self):
        result = add_to_watchlist("600519", tags=["消费", "白马"])
        assert result['symbol'] == '600519'
        assert len(result['tags']) == 2

    def test_get_watchlist_alerts(self):
        result = get_watchlist_alerts()
        assert isinstance(result, list)


class TestXueqiuSkills:
    """雪球调仓 2 skills"""

    def test_get_xueqiu_quote_no_token(self):
        result = get_xueqiu_quote("600519")
        # 无 token 应返回 error 或 dict
        assert isinstance(result, dict)

    def test_track_xueqiu_portfolio(self):
        result = track_xueqiu_portfolio("ZH123456")
        assert isinstance(result, dict)