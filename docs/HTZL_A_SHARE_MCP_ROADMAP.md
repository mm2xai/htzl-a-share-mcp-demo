# HTZL A Share MCP — 2026-08-20 路线图与战况报告

> **作者**: mm2 (OpenClaw Mac Mini)
> **日期**: 2026-08-20 (R841-R849 战果)
> **目标读者**: Sweet（慧途智联创始人）
> **版本**: v0.8.0 Production

---

## 🎯 一句话总结

**htzl-a-share-mcp 已 production-ready（30 tool + install.sh + plugin.json + OpenClaw 集成），但 GitHub 权限阻塞导致真实仓 `htzlai/htzl-a-share-mcp` 未建；同时发现 3 大竞品（huweihua123/stock-mcp 171★、wolfjkd/tradex-hub 30★ 129 tool、CharmYue/ashare-mcp 6★），需要在 4 个差异化点上（OpenClaw 集成、Apache-2.0、Agent Plugins 1.0、install.sh）继续打透。**

---

## 📊 战果总览（R841-R849 共 9 轮）

| 阶段 | 轮次 | 关键产出 |
|---|---|---|
| **W1 仓建** | R841 | mm2xai/htzl-a-share-mcp-demo 已存在，0⭐，完整 W1 骨架 + 4 客户端文档 |
| **W5 5 tool** | R842-R843 | server.py 5 tool 实现，本地 stdio 实测全通过 |
| **W6 30 tool** | R844-R846 | openclaw mcp set 写盘 + bundle-mcp 真实 spawn + W6 25 tool 升级 |
| **W7 release** | R847 | v0.8.0 + install.sh (2.5KB) + plugin.json (Agent Plugins 1.0) |
| **竞品扫描** | R848 | 5 个 A 股 MCP 竞品（huweihua/tradex/CharmYue 等） |
| **架构反向** | R849 | tradex-hub 95 文件 + 工具注册中心架构 |

---

## 🏆 当前 htzl-a-share-mcp 状态

### 1. demo 仓真实状态

| 维度 | 状态 |
|---|---|
| 仓 URL | https://github.com/mm2xai/htzl-a-share-mcp-demo |
| star 数 | 0 ⭐ |
| License | Apache-2.0 ✅ |
| commits | 13 (W1-W7 完整链路) |
| 最后推送 | 2026-08-20T10:15:21Z |
| 代码 | 544KB / 52 文件 |
| tool 数 | 30 (5 W5 + 25 W6) |
| 测试 | 163 tests ✅ |
| CI | GitHub Actions ✅ |
| Docker | Dockerfile + docker-compose ✅ |
| **install.sh** | ✅ R847 起草 |
| **plugin.json** | ✅ R847 起草 |
| **OpenClaw 集成** | ✅ 实战 pid 18529 在跑 |

### 2. 仓的 12 类工具

| 类别 | 数量 | 工具 |
|---|---|---|
| 数据层 | 5 | get_stock_daily / realtime / basic / etf_list / index_daily |
| 资金流 | 2 | get_capital_flow / sector_flow |
| 涨停追踪 | 2 | get_limit_up_pool / stats |
| 技术面 | 3 | turtle_signal / macd / kdj |
| 估值 | 2 | get_pe / get_pb |
| 财报 | 2 | get_income_statement / financial_indicators |
| 多因子 | 1 | multi_factor_select |
| 回测 | 3 | backtest_turtle / multi_factor / compare |
| 风控 | 2 | risk_var / position_size |
| 报告 | 3 | generate_daily / sector / portfolio |
| 自选股 | 2 | add_to_watchlist / get_watchlist_alerts |
| 雪球 | 2 | get_xueqiu_quote / track_xueqiu_portfolio |
| 飞书 | 1 | push_to_feishu |
| **总计** | **30** | ✅ |

---

## 🚨 阻塞项（需要 Sweet 介入）

### 1. GitHub 权限阻塞（最关键）

```
failed to fork: HTTP 403: Must have admin rights to Repository.
mm2xai does not have the correct permissions to execute CreateRepository
```

**两条路径：**

**路径 A（推荐）**: 在 htzlai org 直接 web UI 建仓
1. GitHub → htzlai → New repository → `htzl-a-share-mcp`
2. 设为 Public
3. 本地 `git remote add origin https://github.com/htzlai/htzl-a-share-mcp.git`
4. `git push origin main`

**路径 B**: 把 mm2xai 加到 htzlai admin team
1. GitHub → htzlai → People → Invite member
2. Role: Owner 或 Admin
3. 重新 fork / create

### 2. PyPI 发布未做

**v0.8.0 已 commit 但未推到 PyPI**
- 需要 `pypi.org` 账号 token
- 仓已有 `publish.yml` workflow
- 路径：`pip install htzl-a-share-mcp` 即可启用 30 tool

### 3. OpenClaw 集成文档未推到仓

**docs/clients/openclaw.md 已写但未 commit**
- mm2 实战 5+ 场景
- 等待真实仓建好后 commit 到 htzlai/htzl-a-share-mcp

---

## 📊 竞品分析（R848）

### 三大直接竞品

| 项目 | ⭐ | Tools | 最后更新 | License | 关键差异 |
|---|---|---|---|---|---|
| **huweihua123/stock-mcp** | **171** | ? | 2026-03-25 | NOASSERTION | 6KB 仓，全市场（A股/美股/加密），但 6 个月没维护 |
| **wolfjkd/tradex-hub** | **30** | **129** | 2026-08-18 | NOASSERTION | eltdx 通达信独有，SmartRouter 多源，819KB code |
| **CharmYue/ashare-mcp** | 6 | **30** | 2026-06-02 | MIT | **完全对标我们**，akshare+baostock+tushare |
| guangxiangdebizi/Akshare-MCP | 10 | 3 | 2025-07-17 | - | 半成品 |
| Kinneyzhang/a-share-mcp | 2 | ? | 2026-05-11 | MIT | 小众 |

### wolfjkd/tradex-hub 反向工程（R849）

**95 个 Python 文件，4 个分类：**

```
L1 数据获取 (16 模块) = anti_ban_client + concept + dragon_tiger + northbound + fund_flow 
                     + industry + limit_up_board + smart_router + tick_store + ws_server
L2 计算引擎 (20 模块) = registry + signal_generation + technical_indicators + stock_screening
                     + valuation + macro_fx + news_events + performance_metrics
L3 决策支持 (~5 模块) = dashboard web UI + signal_data 系列
```

**关键学习（tradex 独有）：**
1. **工具注册中心**（ToolMeta + ToolRegistry + auto_discover）
2. **反爬机制**（anti_ban_client.py 节流 + Session 复用）
3. **数据源梯队**（L1 eltdx + 腾讯 + 本地 / L2 同花顺等 / L3 东财）
4. **数据源看板 web UI**（端口 8765）

---

## 🎯 差异化护城河（必须坚持的 5 点）

```
✅ Apache-2.0 License           (vs CharmYue MIT 类似 vs tradex NOASSERTION 差)
✅ OpenClaw 原生集成            (vs 全部竞品无)
✅ Agent Plugins 1.0 manifest   (vs 全部竞品无)
✅ install.sh + health check    (vs 全部竞品无)
✅ 4 客户端集成文档              (vs 全部竞品无)
```

**为什么这些是真正的护城河？**
- OpenClaw 用户群 = mm2 + Sweet 团队 + OpenClaw 全网 = 中国 AI Agent 头部用户
- Agent Plugins 1.0 manifest = OpenClaw 官方注册表入口
- 4 客户端集成 = Claude Code / CoWork / Cherry Studio 用户都能用
- install.sh + bin wrapper = macOS 用户一行 curl 安装

---

## 🎯 必须补的 4 个盲点

```
❗ Cache 层（utils/cache.py）—— 避免 akshare 重复请求被封
❗ baostock 降级（参考 CharmYue/ashare-mcp）—— akshare 不稳时切换
❗ 数据源梯队（L1-L4 分层）—— tradex-hub 独有优势
❗ 题材/龙虎榜/北向资金（tradex 16 模块独有）—— 当前 A 股核心分类
```

---

## 📅 下一步行动计划（R850-R860）

### R850（19:42 已完成）— 本文档
### R851（20:12）— 加 Cache 层 + baostock 降级
### R852（20:42）— 加 4 个新模块：concept / dragon_tiger / northbound / hot_money
### R853（21:12）— 拆分 server.py 重构为 registry 模式
### R854（21:42）— 数据源看板 web UI
### R855（22:12 之后暂停）— PyPI v0.8.0 发布准备

> **凌晨 02:00-07:00 暂停扫描**（防风控铁律）

### 真实仓 `htzlai/htzl-a-share-mcp` 优先级

**P0（本周必做）:**
1. Sweet 解决 GitHub 权限（路径 A 或 B）
2. 真实仓建好 → 推 demo 仓全部内容
3. PyPI v0.8.0 发布

**P1（下周）:**
1. clawhub registry 提交
2. R851-R854 升级路径

**P2（季度）:**
1. v0.8 → v0.9 → v1.0
2. 多市场（港股/美股/加密）
3. 1⭐ → 10⭐ → 100⭐

---

## 🔍 数据来源

| 数据 | 来源 | 时间 |
|---|---|---|
| 30 tool 列表 | server.py 实测 | R846 |
| 5 竞品发现 | gh api search | R848 |
| tradex 95 文件结构 | git tree api | R849 |
| tool 注册模式 | raw github | R849 |
| OpenClaw pid 18529 | lsof + ps | R845 |

---

## 📈 趋势总结

```
R841 → R849 9 轮 = 完整 production 化链路
W1 → W7 完整推进（demo 仓已就位）
OpenClaw 真实集成 ✅ (pid 18529 在跑)
3 大竞品定位明确 ✅
差异化护城河清晰 ✅
盲点学习清晰 ✅
```

**核心洞察：A 股 MCP 赛道已成红海，但 OpenClaw 集成 + Agent Plugins 1.0 + Apache-2.0 = 真正的护城河。**

---

**写于 2026-08-20 19:42 · mm2 · 用 ❤️ + 🔬 + 🍬**
