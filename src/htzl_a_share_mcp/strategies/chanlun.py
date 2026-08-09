"""缠论核心策略"""


class Fractal:
    """分型：顶分型/底分型"""

    def __init__(self, date, price, fractal_type):
        self.date = date
        self.price = price
        self.fractal_type = fractal_type  # 'top' or 'bottom'


class ChanlunStrategy:
    """缠论核心策略"""

    def identify_fractals(self, df):
        """识别分型"""
        fractals = []
        for i in range(1, len(df) - 1):
            if df.iloc[i]['high'] > df.iloc[i-1]['high'] and df.iloc[i]['high'] > df.iloc[i+1]['high']:
                fractals.append(Fractal(df.iloc[i]['date'], df.iloc[i]['high'], 'top'))
            elif df.iloc[i]['low'] < df.iloc[i-1]['low'] and df.iloc[i]['low'] < df.iloc[i+1]['low']:
                fractals.append(Fractal(df.iloc[i]['date'], df.iloc[i]['low'], 'bottom'))
        return fractals

    def identify_strokes(self, fractals):
        """识别笔（顶底交替）"""
        strokes = []
        for i in range(len(fractals) - 1):
            if fractals[i].fractal_type != fractals[i+1].fractal_type:
                direction = 'up' if fractals[i].fractal_type == 'bottom' else 'down'
                strokes.append((fractals[i], fractals[i+1], direction))
        return strokes