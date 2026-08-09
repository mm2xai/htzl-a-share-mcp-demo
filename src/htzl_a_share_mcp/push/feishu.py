"""飞书推送器"""
from typing import Optional

try:
    import requests
except ImportError:
    requests = None


class FeishuPusher:
    """飞书推送器（支持 text / post / interactive 3 种消息类型）"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_text(self, content: str) -> dict:
        """发送文本消息"""
        if requests is None:
            raise ImportError("requests not installed")
        payload = {"msg_type": "text", "content": {"text": content}}
        return self._send(payload)

    def send_post(self, title: str, content_lines: list) -> dict:
        """发送富文本消息"""
        if requests is None:
            raise ImportError("requests not installed")
        payload = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [[{"tag": "text", "text": line}] for line in content_lines]
                    }
                }
            },
        }
        return self._send(payload)

    def push_stock_alert(self, symbol: str, alert_type: str, price: float, reason: str) -> dict:
        """股票预警推送（交互式卡片封装）"""
        if requests is None:
            raise ImportError("requests not installed")
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"content": f"🚨 {alert_type} - {symbol}", "tag": "plain_text"}},
                "elements": [
                    {"tag": "div", "text": {"content": f"**股票:** {symbol}\n**价格:** ¥{price:.2f}\n**原因:** {reason}", "tag": "lark_md"}}
                ]
            }
        }
        return self._send(payload)

    def _send(self, payload: dict) -> dict:
        if requests is None:
            raise ImportError("requests not installed")
        response = requests.post(self.webhook_url, json=payload, timeout=10)
        return {"status_code": response.status_code, "response": response.text}