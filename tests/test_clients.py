"""W8-W10 收尾测试（Dockerfile + 4 客户端配置 + docs）"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestDockerArtifacts:
    """Docker 产物测试"""

    def setup_method(self):
        self.root = Path(__file__).parent.parent

    def test_dockerfile_exists(self):
        dockerfile = self.root / "Dockerfile"
        assert dockerfile.exists()

    def test_dockerfile_has_python_312(self):
        content = (self.root / "Dockerfile").read_text()
        assert "python:3.12" in content

    def test_dockerfile_exposes_port_8000(self):
        content = (self.root / "Dockerfile").read_text()
        assert "EXPOSE 8000" in content

    def test_dockerfile_has_healthcheck(self):
        content = (self.root / "Dockerfile").read_text()
        assert "HEALTHCHECK" in content

    def test_docker_compose_exists(self):
        compose = self.root / "docker-compose.yml"
        assert compose.exists()

    def test_docker_compose_uses_port_8000(self):
        content = (self.root / "docker-compose.yml").read_text()
        assert "8000:8000" in content


class TestClientConfigs:
    """4 大客户端配置测试"""

    def setup_method(self):
        self.clients_dir = Path(__file__).parent.parent / "docs" / "clients"

    def test_claude_code_config_exists(self):
        assert (self.clients_dir / "claude-code.md").exists()

    def test_cowork_config_exists(self):
        assert (self.clients_dir / "cowork.md").exists()

    def test_openclaw_config_exists(self):
        assert (self.clients_dir / "openclaw.md").exists()

    def test_cherry_studio_config_exists(self):
        assert (self.clients_dir / "cherry-studio.md").exists()

    def test_claude_code_uses_stdio(self):
        content = (self.clients_dir / "claude-code.md").read_text()
        assert "stdio" in content
        assert "mcp_servers.json" in content

    def test_cowork_uses_streamable_http(self):
        content = (self.clients_dir / "cowork.md").read_text()
        assert "streamable-http" in content
        assert "8000" in content

    def test_openclaw_uses_stdio(self):
        content = (self.clients_dir / "openclaw.md").read_text()
        assert "stdio" in content

    def test_cherry_studio_uses_stdio(self):
        content = (self.clients_dir / "cherry-studio.md").read_text()
        assert "stdio" in content

    def test_all_4_clients_documented(self):
        """4 大客户端必须全部文档化"""
        clients = ["claude-code", "cowork", "openclaw", "cherry-studio"]
        for c in clients:
            assert (self.clients_dir / f"{c}.md").exists(), f"缺少 {c}"


class TestDocs:
    """docs/ 目录完整性测试"""

    def setup_method(self):
        self.docs_dir = Path(__file__).parent.parent / "docs"

    def test_docs_dir_exists(self):
        assert self.docs_dir.exists()

    def test_clients_subdir_exists(self):
        assert (self.docs_dir / "clients").exists()

    def test_at_least_5_docs_files(self):
        md_files = list(self.docs_dir.rglob("*.md"))
        assert len(md_files) >= 5, f"docs 至少 5 个 md 文件，实际 {len(md_files)}"