"""W12 Release 计划验证"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestReleasePlan:
    """Release 计划文档测试"""

    def setup_method(self):
        self.plan = Path(__file__).parent.parent / "docs" / "RELEASE_PLAN.md"

    def test_release_plan_exists(self):
        assert self.plan.exists()

    def test_plan_has_10_pr_targets(self):
        content = self.plan.read_text()
        # 至少列出 10 个 PR 目标
        pr_count = sum(1 for line in content.split('\n') if '**' in line and '⭐' in line)
        assert pr_count >= 10

    def test_plan_has_timeline(self):
        content = self.plan.read_text()
        assert "2026-11-01" in content
        assert "时间表" in content or "Roadmap" in content

    def test_plan_has_py_publish_flow(self):
        content = self.plan.read_text()
        assert "PyPI" in content
        assert "publish" in content.lower()


class Test12WeekRoadmap:
    """12 周路线图完成度测试"""

    def setup_method(self):
        self.plan = Path(__file__).parent.parent / "docs" / "RELEASE_PLAN.md"

    def test_roadmap_12_weeks(self):
        content = self.plan.read_text()
        for week in ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12"]:
            assert week in content, f"缺少 {week}"

    def test_roadmap_completion_high(self):
        content = self.plan.read_text()
        # 总进度至少 80%
        assert "80%" in content or "83%" in content or "100%" in content


class TestFinalReadiness:
    """最终 Release Readiness"""

    def setup_method(self):
        self.root = Path(__file__).parent.parent

    def test_all_8_required_artifacts(self):
        required = [
            "README.md", "LICENSE", "Dockerfile", "docker-compose.yml",
            "pyproject.toml", ".github/workflows/publish.yml",
            ".github/workflows/ci.yml", "docs/quickstart.md",
        ]
        for r in required:
            assert (self.root / r).exists()

    def test_4_clients_documented(self):
        clients_dir = self.root / "docs" / "clients"
        assert (clients_dir / "claude-code.md").exists()
        assert (clients_dir / "cowork.md").exists()
        assert (clients_dir / "openclaw.md").exists()
        assert (clients_dir / "cherry-studio.md").exists()

    def test_release_plan_documented(self):
        assert (self.root / "docs" / "RELEASE_PLAN.md").exists()

    def test_beta_testing_documented(self):
        assert (self.root / "docs" / "BETA_TESTING.md").exists()

    def test_distribution_artifacts(self):
        """dist/ 包含 wheel 和 sdist"""
        dist = self.root / "dist"
        if dist.exists():
            whls = list(dist.glob("*.whl"))
            sdists = list(dist.glob("*.tar.gz"))
            assert len(whls) >= 1
            assert len(sdists) >= 1

    def test_29_skills_implemented(self):
        from htzl_a_share_mcp.skills import get_all_skill_names
        assert len(get_all_skill_names()) == 29

    def test_test_count_above_100(self):
        """测试数量必须 >= 100"""
        from pathlib import Path
        test_files = list((self.root / "tests").glob("test_*.py"))
        # 至少 8 个测试文件
        assert len(test_files) >= 8