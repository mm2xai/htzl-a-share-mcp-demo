"""HTZL A Share MCP 主服务（FastMCP）"""

import os
import sys
import argparse
from fastmcp import FastMCP


def create_mcp_server(host: str = "0.0.0.0", port: int = 8000) -> FastMCP:
    """创建 MCP 服务器（不启动）"""
    # FastMCP 3.4+: host/port 在 run 时传，不在 __init__
    mcp = FastMCP("htzl-a-share-mcp")

    # 注册 5 skills MVP（W5 阶段）
    from .data_sources import AKShareSource, TushareSource, MockDataSource, DataSourceFailover
    from .strategies import TurtleStrategy, ChanlunStrategy, MultiFactorStrategy
    from .community import XueqiuSource
    from .push import FeishuPusher

    # 初始化（use_mock=True 强制使用 Mock，保证 W5 测试可重复）
    use_mock = os.getenv("HTZL_USE_MOCK", "true").lower() == "true"
    if use_mock:
        failover = DataSourceFailover([MockDataSource(base_price=100.0)])
    else:
        failover = DataSourceFailover([
            AKShareSource(),
            TushareSource(os.getenv("TUSHARE_TOKEN", "")),
            MockDataSource(base_price=100.0),  # 兜底
        ])
    xueqiu = XueqiuSource(os.getenv("XUEQIU_TOKEN", ""))
    turtle = TurtleStrategy()
    multi_factor = MultiFactorStrategy()
    feishu = FeishuPusher(os.getenv("FEISHU_WEBHOOK", ""))

    @mcp.tool()
    def get_stock_daily(symbol: str, start: str, end: str) -> list:
        """获取 A 股日线数据（多源故障转移）"""
        df = failover.get_daily(symbol, start, end)
        return df.to_dict(orient="records")

    @mcp.tool()
    def get_stock_realtime(symbol: str) -> dict:
        """获取 A 股实时行情"""
        return failover.get_realtime(symbol)

    @mcp.tool()
    def turtle_signal(symbol: str, days: int = 60) -> dict:
        """海龟交易法信号"""
        df = failover.get_daily(symbol, "2020-01-01", "2026-12-31")
        signals = turtle.calculate_signals(df.tail(days))
        return {
            "symbol": symbol,
            "buy_signal": bool(signals["buy_signal"].iloc[-1]),
            "sell_signal": bool(signals["sell_signal"].iloc[-1]),
            "N": float(signals["N"].iloc[-1]) if not signals["N"].isna().all() else 0.0,
        }

    @mcp.tool()
    def get_xueqiu_quote(symbol: str) -> dict:
        """通过雪球获取实时行情（需要 token）"""
        try:
            return xueqiu.get_quote(symbol)
        except Exception as e:
            return {"error": str(e), "symbol": symbol}

    @mcp.tool()
    def push_to_feishu(message: str) -> dict:
        """推送消息到飞书（需要 webhook）"""
        try:
            return feishu.send_text(message)
        except Exception as e:
            return {"error": str(e), "message": message}

    # ===== W6 升级：批量挂载 25 个剩余 skill =====
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

    return mcp


def main():
    """主入口：支持 stdio / streamable-http 双模式"""
    parser = argparse.ArgumentParser(description="HTZL A Share MCP")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    mcp = create_mcp_server(host=args.host, port=args.port)

    print(f"🚀 HTZL A Share MCP started (transport={args.transport})", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()