"""Baostock 数据源（参考 CharmYue/ashare-mcp）

Baostock 是国内老牌股票数据接口，无需 token，数据稳定，
作为 akshare 主源失败时的降级方案。
"""
import pandas as pd
from datetime import datetime
from .base import BaseDataSource

try:
    import baostock as bs
except ImportError:
    bs = None


def _baostock_date(d: str) -> str:
    """统一日期格式：YYYY-MM-DD → YYYYMMDD"""
    return d.replace("-", "")


def _to_iso_date(d) -> str:
    """统一日期格式：datetime/str → YYYY-MM-DD"""
    if isinstance(d, str):
        return d
    if hasattr(d, "strftime"):
        return d.strftime("%Y-%m-%d")
    return str(d)


class BaostockSource(BaseDataSource):
    """Baostock 数据源（降级方案）

    特点：
    - 无需 token（注册免费）
    - 数据稳定，老牌
    - akshare 失败时自动降级到 baostock
    """

    _logged_in: bool = False  # 类级别状态：是否已登录

    def __init__(self):
        if bs is None:
            raise ImportError("baostock not installed")
        self._ensure_login()

    @classmethod
    def _ensure_login(cls):
        """确保 baostock 已登录（每次重新登录以确保连接有效）"""
        try:
            bs.logout()
        except Exception:
            pass
        try:
            lg = bs.login()
            if lg.error_code != "0":
                raise RuntimeError(f"baostock login failed: {lg.error_msg}")
            cls._logged_in = True
        except Exception as e:
            cls._logged_in = False
            raise

    def get_daily(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """获取日线数据（前复权）"""
        # 标准化股票代码（沪市加 sh. 深市加 sz.）
        bsymbol = self._normalize_symbol(symbol)

        start_date = _baostock_date(start)
        end_date = _baostock_date(end)

        try:
            rs = bs.query_history_k_data_plus(
                bsymbol,
                "date,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="2",  # 前复权
            )
        except Exception as e:
            raise RuntimeError(f"baostock query failed: {e}")

        if rs is None:
            return pd.DataFrame()

        rows = []
        while (rs.error_code == "0") and rs.next():
            rows.append(rs.get_row_data())

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows, columns=rs.fields)
        df = df.rename(columns={
            "date": "日期",
            "open": "开盘",
            "high": "最高",
            "low": "最低",
            "close": "收盘",
            "volume": "成交量",
            "amount": "成交额",
        })
        # 转数值
        for col in ["开盘", "最高", "最低", "收盘"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["成交量"] = pd.to_numeric(df["成交量"], errors="coerce")
        df["成交额"] = pd.to_numeric(df["成交额"], errors="coerce")

        return df

    def get_realtime(self, symbol: str) -> dict:
        """获取实时行情（baostock 无真正实时，用最近一根 K 线）"""
        # baostock 无实时接口，返回最近一天日线
        bsymbol = self._normalize_symbol(symbol)
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - pd.Timedelta(days=7)).strftime("%Y%m%d")

        try:
            rs = bs.query_history_k_data_plus(
                bsymbol,
                "date,close,volume",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="2",
            )
            if rs is None:
                return {"error": "baostock no response", "symbol": symbol}
            rows = []
            while (rs.error_code == "0") and rs.next():
                rows.append(rs.get_row_data())
        except Exception as e:
            raise RuntimeError(f"baostock realtime failed: {e}")

        if not rows:
            return {"error": "no data", "symbol": symbol}

        latest = rows[-1]
        return {
            "symbol": symbol,
            "date": _to_iso_date(latest[0]),
            "price": float(latest[1]) if latest[1] else 0.0,
            "volume": float(latest[2]) if latest[2] else 0.0,
            "source": "baostock",
        }

    def is_available(self) -> bool:
        """检查 baostock 是否可用"""
        try:
            self._ensure_login()
            return self._logged_in
        except Exception:
            return False

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        """标准化股票代码

        沪市 6/9 开头: sh.600519
        深市 0/3 开头: sz.000001
        """
        if symbol.startswith(("sh.", "sz.", "SH.", "SZ.")):
            return symbol.lower()
        if symbol.startswith(("6", "9")):
            return f"sh.{symbol}"
        if symbol.startswith(("0", "3")):
            return f"sz.{symbol}"
        return symbol.lower()
