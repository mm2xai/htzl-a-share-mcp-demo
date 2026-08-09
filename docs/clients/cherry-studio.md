# Cherry Studio 集成

Cherry Studio 支持 stdio MCP servers。

## 配置步骤

1. 打开 Cherry Studio 设置 → MCP Servers
2. 添加新 server：
   - Name: `htzl-a-share`
   - Type: `stdio`
   - Command: `python`
   - Args: `-m htzl_a_share_mcp.server --transport stdio`
3. 保存并启用

## 使用

在 Cherry Studio 对话中引用 HTZL A Share MCP：

```
列出今日涨停股池，并生成板块报告
```

Cherry Studio 自动调用：
- `get_limit_up_pool()` 涨停股池
- `generate_sector_report(sector="...")` 板块报告