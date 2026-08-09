# Claude Code 集成

HTZL A Share MCP 可以通过 stdio 模式与 Claude Code 无缝集成。

## 安装

```bash
# 1. 安装 htzl-a-share-mcp
pip install htzl-a-share-mcp
```

## 配置

在 `~/.claude/mcp_servers.json` 中添加：

```json
{
  "mcpServers": {
    "htzl-a-share": {
      "command": "python",
      "args": ["-m", "htzl_a_share_mcp.server", "--transport", "stdio"],
      "env": {
        "HTZL_USE_MOCK": "false",
        "TUSHARE_TOKEN": "your_token_here",
        "XUEQIU_TOKEN": "your_token_here",
        "FEISHU_WEBHOOK": "your_webhook_here"
      }
    }
  }
}
```

## 使用示例

在 Claude Code 中：

```
帮我分析贵州茅台（600519）的当前估值和最近一周的资金流向
```

Claude Code 会自动调用：
- `get_pe(symbol="600519")` 获取 PE 估值
- `get_capital_flow(symbol="600519", days=7)` 获取 7 日资金流向
- `generate_daily_report(symbol="600519")` 生成日报