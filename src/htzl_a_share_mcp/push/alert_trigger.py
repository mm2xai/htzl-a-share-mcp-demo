"""预警触发器"""
from typing import Dict, List
from .feishu import FeishuPusher


class AlertTrigger:
    """预警触发器（关联飞书推送）"""

    def __init__(self, feishu_pusher: FeishuPusher):
        self.feishu = feishu_pusher

    def on_price_alert(self, symbol: str, current_price: float, threshold_price: float, direction: str) -> dict:
        """价格预警"""
        if direction == "up" and current_price >= threshold_price:
            return self.feishu.push_stock_alert(symbol, "价格突破", current_price, f"突破 {threshold_price}")
        if direction == "down" and current_price <= threshold_price:
            return self.feishu.push_stock_alert(symbol, "价格跌破", current_price, f"跌破 {threshold_price}")
        return {"status": "no_alert"}

    def on_signal_alert(self, symbol: str, signal: Dict) -> dict:
        """策略信号预警"""
        if signal.get('buy_signal'):
            return self.feishu.push_stock_alert(symbol, "买入信号", signal.get('price', 0), str(signal))
        if signal.get('sell_signal'):
            return self.feishu.push_stock_alert(symbol, "卖出信号", signal.get('price', 0), str(signal))
        return {"status": "no_alert"}