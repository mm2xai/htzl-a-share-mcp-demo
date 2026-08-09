"""雪球数据源"""
from typing import Dict, List

try:
    import pysnowball as ball
except ImportError:
    ball = None


class XueqiuSource:
    """雪球数据源（基于 pysnowball）"""

    def __init__(self, token: str):
        self.token = token
        if ball and token:
            ball.set_token(f"xq_a_token={token}")

    def get_quote(self, symbol: str) -> Dict:
        if ball is None:
            raise ImportError("pysnowball not installed")
        return ball.quote(symbol)

    def get_kline(self, symbol: str, period: str = "day", count: int = -284):
        if ball is None:
            raise ImportError("pysnowball not installed")
        return ball.kline(symbol, period=period, count=count)

    def get_hot_stocks(self, count: int = 100) -> List[Dict]:
        if ball is None:
            raise ImportError("pysnowball not installed")
        return ball.hot_stock(count=count)