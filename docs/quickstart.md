# HTZL A Share MCP 快速入门

## 5 分钟跑通

```bash
# 1. 安装
pip install htzl-a-share-mcp

# 2. 启动 stdio 模式
python -m htzl_a_share_mcp.server --transport stdio

# 3. 或启动 HTTP 模式
python -m htzl_a_share_mcp.server --transport streamable-http --host 0.0.0.0 --port 8000
```

## 5 分钟测试

```python
from htzl_a_share_mcp.skills import (
    get_stock_daily, turtle_signal, multi_factor_select,
    get_pe, generate_daily_report
)

# 日线数据
daily = get_stock_daily("600519", "2025-01-01", "2025-12-31")
print(f"贵州茅台 2025 年共 {len(daily)} 个交易日")

# 海龟信号
signal = turtle_signal("600519")
print(f"海龟信号: {signal}")

# 多因子选股
top5 = multi_factor_select(top_n=5)
print(f"TOP 5: {top5}")

# PE 估值
pe = get_pe("600519")
print(f"PE: {pe}")

# 生成日报
report = generate_daily_report("600519")
print(f"日报: {report}")
```

## 下一步

- 阅读 [Claude Code 集成](clients/claude-code.md)
- 阅读 [CoWork 集成](clients/cowork.md)
- 阅读 [OpenClaw 集成](clients/openclaw.md)
- 阅读 [Cherry Studio 集成](clients/cherry-studio.md)