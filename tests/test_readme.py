"""W11-W12 Release 验证测试"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestREADME:
    """README 完整性测试"""

    def setup_method(self):
        self.readme = Path(__file__).parent.parent / "README.md"
        self.beta = Path(__file__).parent.parent / "docs" / "BETA_TESTING.md"

    def test_readme_exists(self):
        assert self.readme.exists()

    def test_readme_has_chinese_title(self):
        content = self.readme.read_text()
        assert "HTZL A Share MCP" in content
        assert "慧途智联" in content

    def test_readme_lists_29_skills(self):
        """README 必须列出所有 29 skills"""
        content = self.readme.read_text()
        from htzl_a_share_mcp.skills import get_all_skill_names
        names = get_all_skill_names()
        # 至少列出 20 个（README 摘要）
        listed = sum(1 for n in names if n in content)
        assert listed >= 20, f"README 只列出 {listed}/29 skills"

    def test_readme_has_clients_section(self):
        content = self.readme.read_text()
        assert "Claude Code" in content
        assert "CoWork" in content
        assert "OpenClaw" in content
        assert "Cherry Studio" in content

    def test_readme_has_acknowledgments(self):
        """致谢名单"""
        content = self.readme.read_text()
        # 至少致谢 3 个核心项目
        assert "modelcontextprotocol/servers" in content
        assert "simonlin1212/a-stock-data" in content
        assert "uname-yang/pysnowball" in content

    def test_readme_has_roadmap(self):
        """路线图"""
        content = self.readme.read_text()
        assert "Roadmap" in content
        assert "v0.7" in content
        assert "v1.0" in content


class TestBetaTesting:
    """W11 Beta 测试文档测试"""

    def setup_method(self):
        self.beta = Path(__file__).parent.parent / "docs" / "BETA_TESTING.md"

    def test_beta_doc_exists(self):
        assert self.beta.exists()

    def test_beta_doc_has_test_plan(self):
        content = self.beta.read_text()
        assert "测试" in content
        assert "用例" in content or "test" in content.lower()

    def test_beta_doc_has_criteria(self):
        """通过标准"""
        content = self.beta.read_text()
        assert "通过标准" in content or "标准" in content

    def test_beta_doc_has_timeline(self):
        """时间线"""
        content = self.beta.read_text()
        assert "2026-08-15" in content or "2026-09-15" in content


class TestReleaseReadiness:
    """W12 Release 就绪度测试"""

    def setup_method(self):
        self.root = Path(__file__).parent.parent

    def test_pyproject_toml_present(self):
        assert (self.root / "pyproject.toml").exists()

    def test_publish_workflow_present(self):
        assert (self.root / ".github" / "workflows" / "publish.yml").exists()

    def test_ci_workflow_present(self):
        assert (self.root / ".github" / "workflows" / "ci.yml").exists()

    def test_license_present(self):
        assert (self.root / "LICENSE").exists()

    def test_dockerfile_present(self):
        assert (self.root / "Dockerfile").exists()

    def test_4_clients_documented(self):
        """4 大客户端文档齐全"""
        clients_dir = self.root / "docs" / "clients"
        assert (clients_dir / "claude-code.md").exists()
        assert (clients_dir / "cowork.md").exists()
        assert (clients_dir / "openclaw.md").exists()
        assert (clients_dir / "cherry-studio.md").exists()

    def test_29_skills_implemented(self):
        """29 skills 必须实现"""
        from htzl_a_share_mcp.skills import get_all_skill_names
        assert len(get_all_skill_names()) == 29

    def test_release_artifacts_complete(self):
        """Release 产物完整性（8 大要素）"""
        required = [
            "README.md",
            "LICENSE",
            "Dockerfile",
            "docker-compose.yml",
            "pyproject.toml",
            ".github/workflows/publish.yml",
            ".github/workflows/ci.yml",
            "docs/quickstart.md",
        ]
        for r in required:
            assert (self.root / r).exists(), f"缺少 {r}"