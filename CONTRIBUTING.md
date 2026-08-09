# Contributing to htzl-a-share-mcp

🎉 感谢您考虑贡献 htzl-a-share-mcp！

## 报告 Bug

发现 bug？请[提交 Issue](https://github.com/mm2xai/htzl-a-share-mcp-demo/issues/new?template=bug_report.md) 并附上：
- 复现步骤
- 预期 vs 实际
- 环境信息（Python / akshare / tushare 版本）

## 提 Feature Request

有想法？请[提交 Issue](https://github.com/mm2xai/htzl-a-share-mcp-demo/issues/new?template=feature_request.md) 说明：
- Use case
- 优先级 (P0/P1/P2/P3)
- 期望的 API

## 提交 Pull Request

1. Fork 仓库
2. 创建分支 (`git checkout -b feature/my-new-skill`)
3. 编写代码（遵循 [README.md](README.md) 的代码风格）
4. 添加测试 (`tests/test_<module>.py`)
5. 运行测试 (`pytest tests/ -v`)
6. 提交 (`git commit -m 'feat: add my_new_skill'`)
7. Push (`git push origin feature/my-new-skill`)
8. [创建 PR](https://github.com/mm2xai/htzl-a-share-mcp-demo/pulls)

## 添加新 Skill

```python
# src/htzl_a_share_mcp/skills.py
def my_new_skill(symbol: str) -> dict:
    """My new skill description.

    Args:
        symbol: Stock symbol like "600519"

    Returns:
        dict with skill results
    """
    # 实现
    return {"symbol": symbol, "result": "..."}

# 注册到 ALL_SKILLS
ALL_SKILLS["my_new_skill"] = my_new_skill
```

## 测试要求

- 所有 148 个测试必须通过
- 新功能必须添加测试
- 测试覆盖率 ≥ 80%

## 行为准则

请阅读并遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 联系方式

- GitHub Issues: https://github.com/mm2xai/htzl-a-share-mcp-demo/issues
- 邮件: 通过 GitHub 联系

---

再次感谢您的贡献！🌟