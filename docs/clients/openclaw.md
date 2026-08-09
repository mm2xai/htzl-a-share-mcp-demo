# OpenClaw 集成（mm2 自家）

HTZL A Share MCP 原生支持 OpenClaw 平台。

## 配置

在 `~/.openclaw/openclaw.json` 中添加 MCP servers 配置：

```json
{
  "mcpServers": {
    "htzl-a-share": {
      "command": "python",
      "args": ["-m", "htzl_a_share_mcp.server", "--transport", "stdio"],
      "env": {
        "HTZL_USE_MOCK": "true"
      }
    }
  }
}
```

## mm2 已用场景

1. **小红书笔记草稿生成** —— 调用 `generate_daily_report` 写入 docs/xhs-drafts/
2. **每日复盘** —— 调用 `generate_portfolio_report` 推送飞书
3. **选题灵感** —— 调用 `get_limit_up_pool` + `get_sector_flow`