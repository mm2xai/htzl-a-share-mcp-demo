# Claude CoWork 集成

HTZL A Share MCP 通过 streamable-http 模式与 Claude CoWork 集成。

## 部署服务端

```bash
# 使用 Docker
docker-compose up -d

# 或直接运行
python -m htzl_a_share_mcp.server --transport streamable-http --host 0.0.0.0 --port 8000
```

## 配置 CoWork

在 CoWork MCP 配置中添加：

```json
{
  "name": "htzl-a-share",
  "url": "http://localhost:8000/mcp",
  "transport": "streamable-http"
}
```

## 使用示例

```
查看今天沪深300的资金流向，并找出主力净流入 TOP 5 板块
```

CoWork 调用：
- `get_sector_flow(sector="沪深300")` 板块资金流
- `multi_factor_select(top_n=5)` 多因子选股
- `get_capital_flow(symbol=...)` 个股资金流