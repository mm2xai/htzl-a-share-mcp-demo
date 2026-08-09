# HTZL A Share MCP v0.8 路线图

**目标版本：** v0.8.0 (2027-02-01)
**当前版本：** v0.7.0 (2026-11-01)
**目标 stars：** 100+

## v0.8 核心方向

### 1. 多市场扩展（覆盖 7 大市场）
- ✅ A 股（沪深京 5,400+）
- 🆕 港股（恒生 2,200+）
- 🆕 美股（NASDAQ/NYSE 8,000+）
- 🆕 加密货币（BTC/ETH + Top 100 Alt）
- 🆕 外汇（EUR/USD 等 8 大主要货币对）
- 🆕 期货（商品期货 + 金融期货）
- 🆕 ETF（全球 6,000+ ETF）

### 2. LLM 增强选股
- **新闻情绪分析** —— 通过 Anthropic API 实时解析财经新闻
- **财报智能解读** —— Claude 自动提取财报关键洞察
- **研报 AI 摘要** —— 自动化研报摘要生成
- **智能问答** —— "哪些白酒股最近被低估？"

### 3. 高级策略
- **CTA 策略** —— 商品期货策略
- **高频做市** —— 限价单 + 撤单优化
- **多周期共振** —— 日线 + 60min + 15min 三周期共振
- **机器学习** —— XGBoost/LightGBM 因子合成

### 4. 工程能力提升
- **PostgreSQL 数据持久化** —— 历史数据存储
- **Redis 实时缓存** —— 实时行情缓存
- **ClickHouse 列式存储** —— 量化因子存储
- **WebSocket 实时推送** —— 替代 akshare polling

## v0.8 skills 增量（29 → 36）

### 新增 7 个 skills

#### 港股（3）
- `get_hk_stock_daily` - 港股日线
- `get_hk_stock_realtime` - 港股实时
- `hk_turtle_signal` - 港股海龟

#### 美股（2）
- `get_us_stock_daily` - 美股日线
- `get_us_stock_realtime` - 美股实时

#### 加密货币（1）
- `get_crypto_realtime` - BTC/ETH 实时 + Top 100

#### LLM 增强（1）
- `llm_analyze_news` - LLM 新闻情绪分析

## v0.8 → v0.7 对比

| 维度 | v0.7 | v0.8 |
|---|---|---|
| Skills 数 | 29 | 36 |
| 覆盖市场 | A 股 | 7 大市场 |
| 数据源 | akshare + tushare + mock | + yahoo + binance + coingecko |
| 存储 | 无 | PostgreSQL + Redis |
| LLM | 无 | ✅ Anthropic 集成 |
| 性能 | 200ms/查询 | <100ms/查询（缓存） |
| 测试 | 135 | 200+ |
| Stars 目标 | 100 | 500 |

## v0.8 → v1.0 演进（2027-11-01）

| 版本 | 日期 | 目标 |
|---|---|---|
| v0.8 | 2027-02 | 7 大市场 + LLM 集成 |
| v0.9 | 2027-05 | 社区化（PR 提交） |
| v0.10 | 2027-08 | 高级策略（CTA/高频/ML） |
| v0.11 | 2027-09 | 性能优化（缓存/并发） |
| v0.12 | 2027-10 | Beta v1.0 RC 测试 |
| **v1.0** | **2027-11-01** | **正式版 · 50+ skills · 1000+⭐** |

## 与 mm2 OpenClaw 集成实战

### 场景 1：每日 A 股早报生成

```python
# mm2 在 7:00 自动调用
from htzl_a_share_mcp.skills import generate_market_brief

brief = generate_market_brief(
    sectors=["新能源", "白酒", "AI"],
    include_limit_up=True,
    include_capital_flow=True,
)

# mm2 写入 docs/xhs-drafts/2026-MM-DD-market-brief.md
```

### 场景 2：小红书笔记草稿自动生成

```python
# mm2 调用策略后端
from htzl_a_share_mcp.skills import multi_factor_select

top5 = multi_factor_select(factors=["pe", "roe", "momentum"], top_n=5)

# mm2 生成小红书笔记
# 标题: "AI 选了 5 只 A 股，看看你买对了吗？"
# 封面: top5 股票代码大字
```

### 场景 3：飞书定时推送

```python
# mm2 每天 16:00 自动调用
from htzl_a_share_mcp.skills import generate_portfolio_report
from htzl_a_share_mcp.community import push_to_feishu

report = generate_portfolio_report(
    symbols=["600519", "000001", "300750"],
    benchmark="沪深300",
)

push_to_feishu(
    webhook=FEISHU_WEBHOOK,
    title=f"每日收盘报告 {date.today()}",
    content=report,
)
```

### 场景 4：复盘 RAG 知识库

```python
# mm2 集成 htzl skills + 向量数据库
from htzl_a_share_mcp.skills import get_limit_up_pool, get_sector_flow

# 抓数据
pools = get_limit_up_pool()
flows = get_sector_flow(sector="新能源")

# 入向量库
embed(pools + flows, doc_id="xhs-2026-MM-DD")
```

## v0.8 验收标准

- ✅ 36 skills 全实现
- ✅ 7 大市场全部接入
- ✅ 200+ 测试全过
- ✅ mm2 OpenClaw 4 大场景跑通
- ✅ PostgreSQL + Redis 部署
- ✅ PyPI v0.8.0 发布
- ✅ 500+ stars

---

## v0.8 → v1.0 时间线

```
2026-11-01  v0.7.0 完整 Release 🏆
    ↓
2027-02-01  v0.8.0 多市场 + LLM 🆕
    ↓
2027-05-01  v0.9.0 社区化
    ↓
2027-08-01  v0.10 高级策略
    ↓
2027-11-01  v1.0.0 正式版 🏆🏆
```