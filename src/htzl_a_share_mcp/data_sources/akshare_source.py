"""AKShare 数据源"""
import pandas as pd
from .base import BaseDataSource

try:
    import akshare as ak
except ImportError:
    ak = None


class AKShareSource(BaseDataSource):
    """AKShare 数据源（A 股首选）"""

    def get_daily(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        if ak is None:
            raise ImportError("akshare not installed")
        return ak.stock_zh_a_hist(
            symbol=symbol, period="daily",
            start_date=start, end_date=end, adjust="qfq"
        )

    def get_realtime(self, symbol: str) -> dict:
        if ak is None:
            raise ImportError("akshare not installed")
        df = ak.stock_zh_a_spot_em().query(f"代码 == '{symbol}'")
        return df.iloc[0].to_dict() if not df.empty else {}

    def is_available(self) -> bool:
        if ak is None:
            return False
        try:
            ak.stock_zh_a_spot_em()
            return True
        except Exception:
            return False