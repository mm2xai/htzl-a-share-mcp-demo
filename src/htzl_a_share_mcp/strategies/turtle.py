"""海龟交易法策略"""
import pandas as pd
import numpy as np


class TurtleStrategy:
    """海龟交易法（A 股适配版）"""

    def __init__(self, n_entry: int = 20, n_exit: int = 10):
        self.n_entry = n_entry
        self.n_exit = n_exit

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算海龟交易信号"""
        df = df.copy()
        df['prev_high'] = df['high'].shift(1)
        df['prev_low'] = df['low'].shift(1)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.abs(df['high'] - df['close'].shift(1)),
            np.abs(df['low'] - df['close'].shift(1))
        )
        df['N'] = df['tr'].rolling(self.n_entry).mean()
        df['entry_high'] = df['high'].rolling(self.n_entry).max().shift(1)
        df['entry_low'] = df['low'].rolling(self.n_entry).min().shift(1)
        df['buy_signal'] = df['close'] > df['entry_high']
        df['sell_signal'] = df['close'] < df['entry_low']
        df['stop_loss'] = df['close'] - 2 * df['N']
        return df

    def calculate_position_size(self, capital: float, N: float, price: float) -> int:
        """计算头寸规模（1% 风险原则）"""
        risk_per_trade = capital * 0.01
        dollar_volatility = N * price
        position_size = int(risk_per_trade / dollar_volatility) if dollar_volatility > 0 else 0
        return max(position_size, 100)