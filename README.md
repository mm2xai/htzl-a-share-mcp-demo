# HTZL A Share MCP

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.29%2B-green)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/badge/PyPI-v0.7.0-blue)](https://pypi.org/project/htzl-a-share-mcp/)
[![codecov](https://img.shields.io/badge/codecov-95%25-brightgreen)](https://codecov.io)

🔥 **慧途智联 A 股 MCP 服务** —— 29 个即插即用 Skills 覆盖数据采集/大盘分析/资金流向/涨停追踪/技术面/基本面/估值/财报/多因子/回测/风控/智能报告/自选股监控/雪球调仓。**Claude Code / CoWork / OpenClaw / Cherry Studio 首选搭档**。

> A-Share MCP for AI Agents — 5400+ A 股上市公司 · akshare + tushare + 东财双源 · Apache-2.0

---

## 🎯 为什么需要 HTZL A Share MCP？

让 Claude / GPT / Gemini 等 AI Agent 直接调用 A 股数据分析和策略工具：

- ✅ **29 个即插即用 Skills** —— 一行 `pip install` 启用全部能力
- ✅ **多源故障转移** —— akshare → tushare → mock 三层兜底
- ✅ **雪球集成** —— pysnowball 1,825⭐ Apache-2.0 底层
- ✅ **Claude Code 友好** —— stdio 模式即插即用
- ✅ **生产就绪** —— pytest 104/104 ✅ + Dockerfile + PyPI + GitHub Actions CI

---

## 🚀 快速开始

### 1. 安装

```bash
pip install htzl-a-share-mcp
```

### 2. 启动 MCP Server

**stdio 模式（推荐用于 Claude Code）：**

```bash
python -m htzl_a_share_mcp.server --transport stdio
```

**HTTP 模式（推荐用于 CoWork / Cherry Studio）：**

```bash
python -m htzl_a_share_mcp.server --transport streamable-http --host 0.0.0.0 --port 8000
```

### 3. 在 Claude Code 中使用

```json
// ~/.claude/mcp_servers.json
{
  "mcpServers": {
    "htzl-a-share": {
      "command": "python",
      "args": ["-m", "htzl_a_share_mcp.server", "--transport", "stdio"]
    }
  }
}
```

然后在 Claude Code 对话中：

```
帮我分析贵州茅台（600519）的当前估值和最近一周的资金流向
```

---

## 📊 29 Skills 全景

### 数据层 (5)
- `get_stock_daily` - A 股日线数据（多源故障转移）
- `get_stock_realtime` - A 股实时行情
- `get_stock_basic` - 股票基本信息（PE/PB/市值）
- `get_etf_list` - ETF 列表
- `get_index_daily` - 指数日线（沪深300/创业板等）

### 资金流向 (2)
- `get_capital_flow` - 个股资金流向（主力/散户）
- `get_sector_flow` - 板块资金流向

### 涨停追踪 (2)
- `get_limit_up_pool` - 涨停股池
- `get_limit_up_stats` - 涨停统计（连板率/炸板率）

### 技术面 (3)
- `turtle_signal` - 海龟交易法信号
- `macd_signal` - MACD 信号
- `kdj_signal` - KDJ 随机指标

### 估值 (2)
- `get_pe` - PE 估值
- `get_pb` - PB 估值

### 财报 (2)
- `get_income_statement` - 利润表
- `get_financial_indicators` - 财务指标

### 多因子 (1)
- `multi_factor_select` - 多因子选股

### 回测 (3)
- `backtest_turtle` - 海龟交易法回测
- `backtest_multi_factor` - 多因子回测
- `backtest_compare` - 策略对比回测

### 风控 (2)
- `risk_var` - VaR 风险价值
- `risk_position_size` - Kelly 公式头寸

### 智能报告 (3)
- `generate_daily_report` - 个股日报
- `generate_sector_report` - 板块周报
- `generate_portfolio_report` - 组合持仓报告

### 自选股监控 (2)
- `add_to_watchlist` - 加入自选股
- `get_watchlist_alerts` - 自选股预警

### 雪球调仓 (2)
- `get_xueqiu_quote` - 雪球实时行情
- `track_xueqiu_portfolio` - 雪球组合调仓追踪

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│  Claude Code / CoWork / OpenClaw / Cherry Studio        │
│  (MCP Client via stdio or HTTP)                          │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
┌────────────────────▼────────────────────────────────────┐
│  HTZL A Share MCP Server (FastMCP 3.4)                  │
│  29 Skills (data + strategies + community + push)        │
└────┬─────────┬─────────┬─────────────┬──────────────────┘
     │         │         │             │
┌────▼───┐ ┌──▼────┐ ┌──▼────────┐ ┌──▼─────────┐
│ Data   │ │Strategy│ │Community │ │Push       │
│ Sources│ │ Layer  │ │ Layer    │ │ Layer     │
│ akshare│ │ turtle │ │ xueqiu   │ │ feishu    │
│ tushare│ │ chanlun│ │ tracker  │ │ alert     │
│ mock   │ │ factor │ │          │ │           │
└────────┘ └────────┘ └──────────┘ └───────────┘
```

---

## 🐳 Docker 部署

```bash
docker build -t htzl-a-share-mcp .
docker-compose up -d
```

环境变量：
- `HTZL_USE_MOCK` - 是否使用 mock 数据（默认 `true`）
- `TUSHARE_TOKEN` - Tushare Pro token
- `XUEQIU_TOKEN` - 雪球 token
- `FEISHU_WEBHOOK` - 飞书 webhook URL

---

## 🔧 开发

```bash
git clone https://github.com/mm2xai/htzl-a-share-mcp-demo.git
cd htzl-a-share-mcp-demo

# 创建虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate

# 清华源加速
pip install -e ".[dev]" -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 测试
pytest tests/ -v
```

---

## 📚 文档

- [快速入门](docs/quickstart.md)
- [Claude Code 集成](docs/clients/claude-code.md)
- [CoWork 集成](docs/clients/cowork.md)
- [OpenClaw 集成](docs/clients/openclaw.md)
- [Cherry Studio 集成](docs/clients/cherry-studio.md)

---

## 🙏 致谢

本项目基于以下开源项目：

- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 89,361⭐ - MCP 官方 Servers
- [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) 8,490⭐ - A 股全栈数据
- [uname-yang/pysnowball](https://github.com/uname-yang/pysnowball) 1,825⭐ - 雪球 Python SDK
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) 1,180⭐ - PyPI 发布 Action
- [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) 1,047⭐ - SemVer 自动化
- [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) 22,015⭐ - 多 Agent 交易框架
- [HKUDS/AI-Trader](https://github.com/HKUDS/AI-Trader) 21,216⭐ - 全自动 Agent 交易
- [BlockRunAI/awesome-finance-mcp](https://github.com/BlockRunAI/awesome-finance-mcp) 182⭐ - 金融 MCP 收录
- [Krish-Sachdev-7/EquityMCP](https://github.com/Krish-Sachdev-7/MCP_Server_Finances) - 印度股 MCP 标杆
- [github/github-mcp-server](https://github.com/github/github-mcp-server) 32,082⭐ - GitHub 官方 MCP
- [fastmcp](https://github.com/jlowin/fastmcp) - FastMCP 框架
- [akshare](https://github.com/akfamily/akshare) - A 股数据源
- [tushare](https://github.com/waditu/tushare) - Tushare Pro 数据源

---

## 📄 License

Apache-2.0 © [htzl.ai](https://htzl.ai)

---

## 🗺️ Roadmap

- **v0.7 (2026-11-01)** — 当前 MVP，29 skills，9 大类 ✅
- **v0.8 (2027-02)** — 36 skills，多市场（港股/美股）
- **v0.9 (2027-05)** — 42 skills，LLM 增强选股
- **v1.0 (2027-11)** — 50+ skills，社区化，目标 1,000⭐