"""多因子选股策略"""
import pandas as pd


class MultiFactorStrategy:
    """多因子选股策略"""

    def calculate_factor_score(self, df: pd.DataFrame, factor: str) -> pd.Series:
        """计算单个因子得分"""
        if factor == "value":
            return -df['pe'].rank(pct=True)
        elif factor == "growth":
            return df['revenue_growth'].rank(pct=True)
        elif factor == "quality":
            return df['roe'].rank(pct=True)
        elif factor == "momentum":
            return df['return_20d'].rank(pct=True)
        return df.get(factor, pd.Series(0.5, index=df.index))

    def select_stocks(self, df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
        """选择 top N 股票"""
        df = df.copy()
        df['composite_score'] = 0.0
        for factor in ['value', 'growth', 'quality', 'momentum']:
            try:
                df['composite_score'] += self.calculate_factor_score(df, factor) * 0.25
            except Exception:
                pass
        df['rank'] = df['composite_score'].rank(ascending=False)
        return df.nsmallest(top_n, 'rank')