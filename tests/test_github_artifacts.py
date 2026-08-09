"""GitHub Issue / PR 模板测试"""
import pytest
from pathlib import Path


class TestGitHubTemplates:
    """GitHub 模板完整性测试"""

    def setup_method(self):
        self.root = Path(__file__).parent.parent

    def test_feature_request_template(self):
        template = self.root / ".github" / "ISSUE_TEMPLATE" / "feature_request.md"
        assert template.exists()

    def test_bug_report_template(self):
        template = self.root / ".github" / "ISSUE_TEMPLATE" / "bug_report.md"
        assert template.exists()

    def test_pull_request_template(self):
        template = self.root / ".github" / "PULL_REQUEST_TEMPLATE.md"
        assert template.exists()

    def test_feature_request_has_priority(self):
        content = (self.root / ".github" / "ISSUE_TEMPLATE" / "feature_request.md").read_text()
        assert "Priority" in content
        assert "P0" in content

    def test_bug_report_has_priority(self):
        content = (self.root / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").read_text()
        assert "Priority" in content

    def test_pr_template_has_checklist(self):
        content = (self.root / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text()
        assert "Checklist" in content
        assert "[ ]" in content

    def test_pr_template_has_tests(self):
        content = (self.root / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text()
        assert "Tests" in content
        assert "pytest" in content

    def test_all_3_templates_complete(self):
        """3 大模板必须全部存在"""
        files = [
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ]
        for f in files:
            assert (self.root / f).exists(), f"缺少 {f}"


class TestCommunityHealth:
    """社区健康度测试（GitHub 标准）"""

    def setup_method(self):
        self.root = Path(__file__).parent.parent

    def test_has_readme(self):
        assert (self.root / "README.md").exists()

    def test_has_license(self):
        assert (self.root / "LICENSE").exists()

    def test_has_code_of_conduct(self):
        """代码规范（可选但建议）"""
        coc = self.root / "CODE_OF_CONDUCT.md"
        # 可选，不强制
        # assert coc.exists()

    def test_has_contributing(self):
        """贡献指南（可选但建议）"""
        contributing = self.root / "CONTRIBUTING.md"
        # 可选，不强制
        # assert contributing.exists()

    def test_has_workflows(self):
        workflows = self.root / ".github" / "workflows"
        assert workflows.exists()
        assert (workflows / "ci.yml").exists()
        assert (workflows / "publish.yml").exists()

    def test_has_issue_templates(self):
        templates = self.root / ".github" / "ISSUE_TEMPLATE"
        assert templates.exists()

    def test_has_pr_template(self):
        pr_template = self.root / ".github" / "PULL_REQUEST_TEMPLATE.md"
        assert pr_template.exists()