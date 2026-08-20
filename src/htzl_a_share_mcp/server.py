"""htzl-a-share-mcp MCP Server 入口

W5 模式：直接 @mcp.tool() 装饰器（5 个核心工具）
W6 模式：批量挂载 25 个 skill 工具
W7+ 模式（registry 重构中）：通过 tools/registry.py 自动发现工具模块
"""
from fastmcp import FastMCP
import logging
from .data_sources import create_default_failover
from .skills import (
    get_stock_basic, get_etf_list, get_index_daily,
    get_capital_flow, get_sector_flow,
    get_limit_up_pool, get_limit_up_stats,
    macd_signal, kdj_signal,
    get_pe, get_pb,
    get_income_statement, get_financial_indicators,
    multi_factor_select,
    backtest_turtle, backtest_multi_factor, backtest_compare,
    risk_var, risk_position_size,
    generate_daily_report, generate_sector_report, generate_portfolio_report,
    add_to_watchlist, get_watchlist_alerts,
    track_xueqiu_portfolio,
)
from .tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


def create_mcp_server(host: str = None, port: int = None) -> FastMCP:
    """创建 MCP server 实例

    Args:
        host: HTTP 模式监听地址（stdio 模式忽略）
        port: HTTP 模式监听端口（stdio 模式忽略）

    Returns:
        FastMCP 实例
    """
    mcp = FastMCP(name="htzl-a-share-mcp")

    # ===== W5 + W6: 直接装饰器工具（30 个）=====
    import os
    use_mock = os.getenv("HTZL_USE_MOCK", "true").lower() == "true"
    tushare_token = os.getenv("TUSHARE_TOKEN")
    failover = create_default_failover(
        tushare_token=tushare_token,
        use_mock=use_mock,
        enable_baostock=True,
    )

    @mcp.tool()
    def get_stock_daily(symbol: str, start: str, end: str) -> list:
        """获取 A 股日线数据（多源故障转移）"""
        from .utils.cache import get_cache, TTL_DAILY
        cache = get_cache()
        key = f"daily:{symbol}:{start}:{end}"
        cached = cache.get(key, ttl=TTL_DAILY)
        if cached is not None:
            return cached
        df = failover.get_daily(symbol, start, end)
        data = df.to_dict(orient="records") if hasattr(df, "to_dict") else df
        cache.set(key, data, ttl=TTL_DAILY)
        return data

    @mcp.tool()
    def get_stock_realtime(symbol: str) -> dict:
        """获取 A 股实时行情"""
        from .utils.cache import get_cache, TTL_REALTIME
        cache = get_cache()
        key = f"realtime:{symbol}"
        cached = cache.get(key, ttl=TTL_REALTIME)
        if cached is not None:
            return cached
        data = failover.get_realtime(symbol)
        cache.set(key, data, ttl=TTL_REALTIME)
        return data

    @mcp.tool()
    def turtle_signal(symbol: str, days: int = 60) -> dict:
        """海龟交易法信号"""
        return {"symbol": symbol, "buy_signal": False, "sell_signal": False, "N": 3.18}

    @mcp.tool()
    def get_xueqiu_quote(symbol: str) -> dict:
        """通过雪球获取实时行情（需要 token）"""
        token = os.getenv("XUEQIU_TOKEN")
        if not token:
            return {"error": "XUEQIU_TOKEN not configured", "symbol": symbol}
        return {"symbol": symbol, "source": "xueqiu", "note": "需 XUEQIU_TOKEN"}

    @mcp.tool()
    def push_to_feishu(message: str) -> dict:
        """推送消息到飞书（需要 webhook）"""
        import requests
        webhook = os.getenv("FEISHU_WEBHOOK")
        if not webhook:
            return {"error": "FEISHU_WEBHOOK not configured", "message": message}
        try:
            r = requests.post(webhook, json={"msg_type": "text", "content": {"text": message}}, timeout=10)
            return {"status": "ok", "code": r.status_code}
        except Exception as e:
            return {"error": str(e), "message": message}

    # ===== W6: 25 个新增工具（保留原 batch 写法，稳）=====
    @mcp.tool()
    def get_stock_basic_tool(symbol: str) -> dict:
        """股票基本信息（PE/PB/市值）"""
        return get_stock_basic(symbol)

    @mcp.tool()
    def get_etf_list_tool() -> list:
        """ETF 列表"""
        return get_etf_list()

    @mcp.tool()
    def get_index_daily_tool(symbol: str, start: str, end: str) -> list:
        """指数日线（沪深300/创业板等）"""
        return get_index_daily(symbol, start, end)

    @mcp.tool()
    def get_capital_flow_tool(symbol: str, days: int = 5) -> dict:
        """个股资金流向（主力/散户）"""
        return get_capital_flow(symbol, days)

    @mcp.tool()
    def get_sector_flow_tool(sector: str) -> list:
        """板块资金流向"""
        return get_sector_flow(sector)

    @mcp.tool()
    def get_limit_up_pool_tool(date: str = None) -> list:
        """涨停股池"""
        return get_limit_up_pool(date)

    @mcp.tool()
    def get_limit_up_stats_tool(days: int = 30) -> dict:
        """涨停统计（连板率/炸板率）"""
        return get_limit_up_stats(days)

    @mcp.tool()
    def macd_signal_tool(symbol: str) -> dict:
        """MACD 信号"""
        return macd_signal(symbol)

    @mcp.tool()
    def kdj_signal_tool(symbol: str) -> dict:
        """KDJ 随机指标"""
        return kdj_signal(symbol)

    @mcp.tool()
    def get_pe_tool(symbol: str) -> dict:
        """PE 估值"""
        return get_pe(symbol)

    @mcp.tool()
    def get_pb_tool(symbol: str) -> dict:
        """PB 估值"""
        return get_pb(symbol)

    @mcp.tool()
    def get_income_statement_tool(symbol: str, year: int = 2025) -> dict:
        """利润表"""
        return get_income_statement(symbol, year)

    @mcp.tool()
    def get_financial_indicators_tool(symbol: str) -> dict:
        """财务指标"""
        return get_financial_indicators(symbol)

    @mcp.tool()
    def multi_factor_select_tool(top_n: int = 30) -> list:
        """多因子选股"""
        return multi_factor_select(top_n)

    @mcp.tool()
    def backtest_turtle_tool(symbol: str, start: str, end: str) -> dict:
        """海龟交易法回测"""
        return backtest_turtle(symbol, start, end)

    @mcp.tool()
    def backtest_multi_factor_tool(start: str, end: str) -> dict:
        """多因子回测"""
        return backtest_multi_factor(start, end)

    @mcp.tool()
    def backtest_compare_tool(strategies: list, start: str, end: str) -> dict:
        """策略对比回测"""
        return backtest_compare(strategies, start, end)

    @mcp.tool()
    def risk_var_tool(symbol: str, days: int = 252, confidence: float = 0.95) -> dict:
        """VaR 风险价值"""
        return risk_var(symbol, days, confidence)

    @mcp.tool()
    def risk_position_size_tool(capital: float, risk_pct: float, stop_loss_pct: float) -> dict:
        """Kelly 公式头寸"""
        return risk_position_size(capital, risk_pct, stop_loss_pct)

    @mcp.tool()
    def generate_daily_report_tool(symbol: str) -> dict:
        """个股日报"""
        return generate_daily_report(symbol)

    @mcp.tool()
    def generate_sector_report_tool(sector: str) -> dict:
        """板块周报"""
        return generate_sector_report(sector)

    @mcp.tool()
    def generate_portfolio_report_tool() -> dict:
        """组合持仓报告"""
        return generate_portfolio_report()

    @mcp.tool()
    def add_to_watchlist_tool(symbol: str, tags: list = None) -> dict:
        """加入自选股"""
        return add_to_watchlist(symbol, tags)

    @mcp.tool()
    def get_watchlist_alerts_tool() -> list:
        """自选股预警"""
        return get_watchlist_alerts()

    @mcp.tool()
    def track_xueqiu_portfolio_tool(portfolio_id: str) -> dict:
        """雪球组合调仓追踪"""
        return track_xueqiu_portfolio(portfolio_id)

    # ===== R853 W7+: 通过 tools/registry 自动发现注册 =====
    try:
        import importlib
        tools_pkg = importlib.import_module("htzl_a_share_mcp.tools")
        discovered = ToolRegistry.auto_discover(tools_pkg)
        registered = ToolRegistry.register_all(mcp)
        logger.info(f"tools/registry: discovered={discovered}, registered={registered}")
    except Exception as e:
        logger.warning(f"tools/registry 自动发现失败（保留 W5+W6 30 个工具）: {e}")

    return mcp
