# Beta Testing Guide (W11)

**测试周期：** 2026-08-15 ~ 2026-09-15（4 周）
**目标：** 验证 29 skills 在真实环境下的稳定性、准确性、性能

## 测试用例模板

```python
# tests/integration/test_real_world.py
import pytest
import os
from htzl_a_share_mcp.skills import *


@pytest.mark.integration
class TestRealWorldScenarios:
    """真实场景集成测试"""

    def test_analyze_600519_full_workflow(self):
        """贵州茅台完整分析链路"""
        # 1. 获取基本信息
        basic = get_stock_basic("600519")
        assert basic['pe'] > 0

        # 2. 获取最近 30 天日线
        daily = get_stock_daily("600519", "2025-07-01", "2025-08-01")
        assert len(daily) >= 20

        # 3. 海龟信号
        turtle = turtle_signal("600519")
        assert 'buy_signal' in turtle

        # 4. 估值
        pe = get_pe("600519")
        assert pe['pe_ttm'] > 0

        # 5. 资金流向
        flow = get_capital_flow("600519")
        assert 'main_net' in flow

        # 6. 生成日报
        report = generate_daily_report("600519")
        assert 'action' in report

    def test_sector_rotation_strategy(self):
        """板块轮动策略"""
        sectors = ["新能源", "白酒", "医药", "科技", "金融"]
        for s in sectors:
            flow = get_sector_flow(s)
            assert isinstance(flow, list)

    def test_limit_up_pool_real(self):
        """涨停股池实盘验证"""
        pool = get_limit_up_pool()
        assert isinstance(pool, list)
        # 应有 5+ 只涨停股
        assert len(pool) >= 5

    def test_watchlist_alert_pipeline(self):
        """自选股预警管道"""
        add_to_watchlist("600519", tags=["消费"])
        add_to_watchlist("000001", tags=["金融"])
        alerts = get_watchlist_alerts()
        assert isinstance(alerts, list)
```

## Beta 测试人员清单

| 人员 | 角色 | 测试场景 | 报告截止 |
|---|---|---|---|
| Sweet | 项目负责人 | 完整链路 + 业务场景 | 2026-09-15 |
| 客户 1 | AI 量化爱好者 | Claude Code 集成 | 2026-09-15 |
| 客户 2 | CoWork 用户 | CoWork 集成 | 2026-09-15 |
| 客户 3 | mm2 用户 | OpenClaw 集成 | 2026-09-15 |

## 反馈模板

```markdown
### Bug Report
- **Skill 名称：** get_pe
- **复现步骤：** 调用 get_pe("600519")
- **预期结果：** 返回 dict
- **实际结果：** 抛 ConnectionError
- **日志：** 见附件
- **环境：** akshare 1.18.83, Python 3.12

### Feature Request
- **需求：** 加 get_stock_quote(symbol) 实时报价
- **场景：** 需要毫秒级实时报价（替代 akshare 延迟 15min）
- **优先级：** P1
```

## 性能基准

| Skill | 平均响应时间 | P95 | 错误率 |
|---|---|---|---|
| get_stock_daily | 200ms | 500ms | <0.1% |
| get_pe | 100ms | 300ms | <0.1% |
| turtle_signal | 50ms | 150ms | 0% |
| generate_daily_report | 300ms | 800ms | <0.5% |

## 通过标准

- ✅ 所有 104 个单元测试通过
- ✅ Beta 测试 4 周无 P0 级别 bug
- ✅ akshare/tushare 接口稳定性 ≥99.5%
- ✅ PyPI v0.7.0 成功发布
- ✅ 至少 5 个外部用户使用

---

**W11 → W12 过渡：** Beta 通过 → 2026-09-15 发布 v0.7.0 PyPI → 2026-11-01 完整 Release