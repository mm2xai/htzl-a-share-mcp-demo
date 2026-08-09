"""多因子选股策略"""
import pandas as pd


class MultiFactorStrategy:
    """多因子选股策略"""

    def calculate_factor_score(self, df: pd.DataFrame, factor: str) -> pd.Series:
        """计算单个因子得分（归一化到 [0, 1]）"""
        if factor == "value":
            if 'pe' not in df.columns:
                return pd.Series(0.5, index=df.index)
            score = 1 - df['pe'].rank(pct=True, na_option='bottom')
            return score.fillna(0.5)
        elif factor == "growth":
            if 'revenue_growth' not in df.columns:
                return pd.Series(0.5, index=df.index)
            score = df['revenue_growth'].rank(pct=True, na_option='bottom')
            return score.fillna(0.5)
        elif factor == "quality":
            if 'roe' not in df.columns:
                return pd.Series(0.5, index=df.index)
            score = df['roe'].rank(pct=True, na_option='bottom')
            return score.fillna(0.5)
        elif factor == "momentum":
            if 'return_20d' not in df.columns:
                return pd.Series(0.5, index=df.index)
            score = df['return_20d'].rank(pct=True, na_option='bottom')
            return score.fillna(0.5)
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