"""雪球组合调仓追踪"""
import time
from typing import List, Dict

try:
    import requests
except ImportError:
    requests = None


class XueqiuPortfolioTracker:
    """雪球组合调仓追踪（自实现，pysnowball 不直接支持）"""

    BASE_URL = "https://xueqiu.com"

    def __init__(self, cookie: str):
        self.cookie = cookie
        self.session = requests.Session() if requests else None
        if self.session:
            self.session.headers.update({
                "User-Agent": "Mozilla/5.0",
                "Cookie": cookie,
            })

    def get_portfolio_rebalance(self, portfolio_id: str) -> List[Dict]:
        """获取组合调仓记录"""
        if not self.session:
            raise ImportError("requests not installed")
        url = f"{self.BASE_URL}/p/{portfolio_id}/rebalance"
        response = self.session.get(url)
        return response.json()

    def track_top_traders(self, trader_ids: List[str]) -> Dict:
        """追踪多个大V调仓"""
        results = {}
        for tid in trader_ids:
            try:
                portfolio = self.get_portfolio_rebalance(tid)
                results[tid] = portfolio
                time.sleep(1)  # 防风控
            except Exception as e:
                results[tid] = {"error": str(e)}
        return results