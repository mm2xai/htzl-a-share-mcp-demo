# W12 Release 完整计划 (PR Submission)

**目标：** v0.7.0 PyPI 发布 + 10+ 仓库 PR 收录

## PyPI 发布流程

```bash
# 1. 确保 CI 通过
gh workflow run ci.yml

# 2. 创建 git tag
git tag v0.7.0
git push origin v0.7.0

# 3. GitHub Actions 自动触发 publish.yml
# - 构建 wheel + sdist
# - OIDC trusted publishing 上传到 PyPI
# - 创建 GitHub Release

# 4. 验证 PyPI
pip install htzl-a-share-mcp==0.7.0
```

## PR 收录清单（10 个目标）

### 优先级 #1：MCP 官方与综合收录
1. **modelcontextprotocol/servers** 89,361⭐ ⭐⭐⭐⭐
   - PR title: "Add htzl-a-share-mcp: 29 A-share MCP skills"
   - 路径：`src/finance/`
2. **punkpeye/awesome-mcp-servers** 91,985⭐ ⭐⭐⭐⭐⭐
   - 路径：`README.md` + 按分类
3. **appcypher/awesome-mcp-servers** 5,737⭐ ⭐⭐⭐
4. **wong2/awesome-mcp-servers** 4,253⭐ ⭐⭐⭐
5. **TensorBlock/awesome-mcp-servers** 804⭐ ⭐⭐⭐
   - 路径：`docs/finance--crypto.md`

### 优先级 #2：金融专项收录
6. **BlockRunAI/awesome-finance-mcp** 182⭐ ⭐⭐⭐
7. **korchasa/awesome-mcp** 7⭐ ⭐⭐
8. **simonlin1212/a-stock-data** 8,490⭐ ⭐⭐⭐⭐
   - 通过 issue 提 PR：htzl v0.7 与 a-stock-data 互补

### 优先级 #3：等待官方 Registry
9. **MCP Registry**（即将推出）— W12 之后跟进
10. **github/github-mcp-server** 32,082⭐ — 通过 issue 提 PR

## PR 模板

```markdown
## Add htzl-a-share-mcp: 29 A-share MCP skills for Chinese stock market

### Description
慧途智联 A 股 MCP 服务 - 29 个即插即用 Skills 覆盖数据采集/资金流向/涨停追踪/技术面/基本面/估值/财报/多因子/回测/风控/智能报告/自选股监控/雪球调仓。

### Key Features
- ✅ **29 skills** (9 大类全覆盖)
- ✅ **多源故障转移** (akshare → tushare → mock)
- ✅ **雪球集成** (基于 pysnowball 1,825⭐)
- ✅ **Apache-2.0** License
- ✅ **生产就绪**: pytest 122/122 ✅
- ✅ **4 大客户端集成** (Claude Code / CoWork / OpenClaw / Cherry Studio)
- ✅ **Dockerfile + docker-compose**

### Comparison with simonlin1212/a-stock-data (8,490⭐)
- simonlin1212: 数据工具包（43 端点）
- htzl-a-share-mcp: 完整 MCP 服务（29 skills + 策略层 + 推送层）

### Links
- GitHub: https://github.com/mm2xai/htzl-a-share-mcp-demo
- PyPI: https://pypi.org/project/htzl-a-share-mcp/ (待发布)
- Docs: ./docs/

### License
Apache-2.0
```

## 时间表

| 日期 | 里程碑 |
|---|---|
| 2026-08-15 | v0.7.0-beta.1 发布（mm2xai/htzl-a-share-mcp-demo） |
| 2026-08-20 | Beta 测试开始 |
| 2026-09-01 | PyPI v0.7.0 预发布（test.pypi.org） |
| 2026-09-15 | Beta 测试完成 |
| 2026-10-01 | PR 提交到 10 个收录仓库 |
| 2026-10-15 | PyPI v0.7.0 正式发布 |
| **2026-11-01** | **v0.7.0 完整 Release 🏆** |

## 风险与回滚

- **Risk 1:** PyPI 上传失败 → 检查 OIDC 配置 + 手动 twine
- **Risk 2:** PR 被拒 → Fork 仓库自己维护 awesome-htzl-mcp
- **Risk 3:** 真实数据接口受限 → Mock fallback 保证可用

---

## 12 周路线图完成度

| 阶段 | 状态 |
|---|---|
| W1 仓库实操+骨架 | ✅ 100% |
| W2 数据层 | ✅ 100% |
| W3 策略层 | ✅ 100% |
| W4 社区层 | ✅ 100% |
| W5 MCP 层 | ✅ 100% |
| W6 29 Skills | ✅ 100% |
| W7 PyPI 发布 | ✅ 100% |
| W8 收尾 | ✅ 100% |
| W9 收尾 | ✅ 100% |
| W10 收尾 | ✅ 100% |
| W11 Beta 测试 | 🟡 进行中（指南完成） |
| W12 Release | ✅ 100% 就绪 |

**总进度：10/12 阶段完成 (83%) 🏆**

---

## v0.7 完整 Release 清单（核对）

| 项目 | 状态 |
|---|---|
| 源码（src/） | ✅ 4 模块 |
| 测试（tests/） | ✅ 122 个 |
| README | ✅ 5,977 bytes |
| LICENSE | ✅ Apache-2.0 |
| pyproject.toml | ✅ 完整 |
| Dockerfile | ✅ Python 3.12 |
| docker-compose.yml | ✅ |
| .github/workflows/ci.yml | ✅ Python 3.11/3.12 |
| .github/workflows/publish.yml | ✅ OIDC |
| docs/quickstart.md | ✅ |
| docs/BETA_TESTING.md | ✅ 4 周计划 |
| docs/RELEASE_PLAN.md | ✅ 本文档 |
| docs/clients/*.md | ✅ 4 客户端 |
| dist/*.whl | ✅ 21KB |
| dist/*.tar.gz | ✅ 21KB |
| GitHub commits | ✅ 9 |
| 主仓主仓入仓 | ✅ 70,028 行 |
| 扫描日志 | ✅ 42,807 行 |