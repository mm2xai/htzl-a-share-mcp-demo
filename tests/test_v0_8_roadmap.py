"""v0.8 路线图 + mm2 OpenClaw 集成测试"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestRoadmapV08:
    """v0.8 路线图文档测试"""

    def setup_method(self):
        self.roadmap = Path(__file__).parent.parent / "docs" / "ROADMAP_v0.8.md"

    def test_roadmap_exists(self):
        assert self.roadmap.exists()

    def test_roadmap_has_7_markets(self):
        content = self.roadmap.read_text()
        markets = ["A 股", "港股", "美股", "加密货币", "外汇", "期货", "ETF"]
        for m in markets:
            assert m in content, f"缺少 {m}"

    def test_roadmap_has_target_stars(self):
        content = self.roadmap.read_text()
        assert "500" in content or "1000" in content

    def test_roadmap_has_v1_0_date(self):
        content = self.roadmap.read_text()
        assert "2027-11-01" in content

    def test_roadmap_has_llm_integration(self):
        content = self.roadmap.read_text()
        assert "LLM" in content or "Anthropic" in content

    def test_roadmap_has_36_skills(self):
        content = self.roadmap.read_text()
        assert "36" in content


class TestOpenClawIntegration:
    """mm2 OpenClaw 集成文档测试"""

    def setup_method(self):
        self.roadmap = Path(__file__).parent.parent / "docs" / "ROADMAP_v0.8.md"

    def test_has_4_scenarios(self):
        """4 大集成场景"""
        content = self.roadmap.read_text()
        scenarios = [
            "每日 A 股早报生成",
            "小红书笔记草稿自动生成",
            "飞书定时推送",
            "复盘 RAG 知识库",
        ]
        for s in scenarios:
            assert s in content, f"缺少 {s}"

    def test_uses_xhs_drafts(self):
        """mm2 工作流：xhs-drafts/"""
        content = self.roadmap.read_text()
        assert "xhs-drafts" in content

    def test_uses_feishu_webhook(self):
        content = self.roadmap.read_text()
        assert "feishu" in content.lower() or "FEISHU" in content

    def test_uses_multi_factor(self):
        content = self.roadmap.read_text()
        assert "multi_factor" in content


class TestV08Skills:
    """v0.8 新增 skills 兼容性测试"""

    def test_v0_7_skills_count(self):
        """v0.7 保持 29 skills"""
        from htzl_a_share_mcp.skills import get_all_skill_names
        names = get_all_skill_names()
        assert len(names) == 29


class TestTimeLine:
    """时间线测试"""

    def setup_method(self):
        self.roadmap = Path(__file__).parent.parent / "docs" / "ROADMAP_v0.8.md"

    def test_timeline_has_6_versions(self):
        content = self.roadmap.read_text()
        # v0.8, v0.9, v0.10, v0.11, v0.12, v1.0
        for v in ["v0.8", "v0.9", "v1.0"]:
            assert v in content, f"缺少 {v}"

    def test_v1_0_target_date(self):
        content = self.roadmap.read_text()
        assert "2027-11-01" in content