"""Mock 数据源（用于单元测试 + 离线开发）"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .base import BaseDataSource


class MockDataSource(BaseDataSource):
    """Mock 数据源（生成合成数据，无需网络）"""

    def __init__(self, base_price: float = 100.0):
        self.base_price = base_price

    def get_daily(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """生成模拟日线数据"""
        dates = pd.date_range(start=start, end=end, freq='D')
        np.random.seed(hash(symbol) % 2**32)
        n = len(dates)
        close = self.base_price + np.cumsum(np.random.randn(n) * 2)
        high = close + np.abs(np.random.randn(n)) * 1.5
        low = close - np.abs(np.random.randn(n)) * 1.5
        open_ = close + np.random.randn(n) * 0.5
        volume = np.random.randint(1000000, 10000000, n)
        return pd.DataFrame({
            'date': dates,
            'open': open_,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume,
        })

    def get_realtime(self, symbol: str) -> dict:
        """生成模拟实时行情"""
        np.random.seed(hash(symbol) % 2**32)
        return {
            'symbol': symbol,
            'name': f'Mock-{symbol}',
            'price': float(self.base_price + np.random.randn() * 5),
            'change_pct': float(np.random.randn() * 3),
            'volume': int(np.random.randint(1000000, 10000000)),
            'timestamp': datetime.now().isoformat(),
        }

    def is_available(self) -> bool:
        """Mock 永远可用"""
        return True