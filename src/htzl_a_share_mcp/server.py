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