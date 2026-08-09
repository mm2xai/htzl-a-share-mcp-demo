"""Tushare 数据源"""
import pandas as pd
from .base import BaseDataSource

try:
    import tushare as ts
except ImportError:
    ts = None


class TushareSource(BaseDataSource):
    """Tushare 数据源（备份）"""

    def __init__(self, token: str):
        self.token = token
        self.pro = ts.pro_api(token) if (token and ts) else None

    def get_daily(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        if not self.pro:
            raise ValueError("Tushare token not configured")
        return self.pro.daily(
            ts_code=symbol,
            start_date=start.replace("-", ""),
            end_date=end.replace("-", "")
        )

    def get_realtime(self, symbol: str) -> dict:
        if not self.pro:
            raise ValueError("Tushare token not configured")
        df = self.pro.realtime_quotes(symbol)
        return df.iloc[0].to_dict() if not df.empty else {}

    def is_available(self) -> bool:
        return self.pro is not None