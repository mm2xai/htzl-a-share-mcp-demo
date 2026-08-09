"""W7 打包发布验证测试"""
import pytest
import sys
import os
import zipfile
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestPackaging:
    """PyPI 打包验证"""

    @classmethod
    def setup_class(cls):
        cls.dist_dir = Path(__file__).parent.parent / "dist"
        cls.wheel = cls.dist_dir / "htzl_a_share_mcp-0.1.0-py3-none-any.whl"
        cls.sdist = cls.dist_dir / "htzl_a_share_mcp-0.1.0.tar.gz"

    def test_dist_dir_exists(self):
        assert self.dist_dir.exists()

    def test_wheel_exists(self):
        assert self.wheel.exists()
        assert self.wheel.stat().st_size > 10_000  # 至少 10K

    def test_sdist_exists(self):
        assert self.sdist.exists()
        assert self.sdist.stat().st_size > 10_000

    def test_wheel_contents(self):
        """wheel 必须包含核心模块"""
        with zipfile.ZipFile(self.wheel) as z:
            names = z.namelist()
            required = [
                "htzl_a_share_mcp/__init__.py",
                "htzl_a_share_mcp/server.py",
                "htzl_a_share_mcp/skills.py",
                "htzl_a_share_mcp/data_sources/__init__.py",
                "htzl_a_share_mcp/strategies/__init__.py",
                "htzl_a_share_mcp/community/__init__.py",
                "htzl_a_share_mcp/push/__init__.py",
            ]
            for r in required:
                assert r in names, f"wheel 缺少 {r}"

    def test_wheel_has_metadata(self):
        """wheel 必须有 METADATA"""
        with zipfile.ZipFile(self.wheel) as z:
            metadata_files = [n for n in z.namelist() if "METADATA" in n]
            assert len(metadata_files) >= 1

    def test_wheel_has_entry_points(self):
        """wheel 必须有 entry_points.txt"""
        with zipfile.ZipFile(self.wheel) as z:
            ep_files = [n for n in z.namelist() if "entry_points" in n]
            assert len(ep_files) >= 1

    def test_wheel_has_license(self):
        """wheel 必须有 LICENSE"""
        with zipfile.ZipFile(self.wheel) as z:
            license_files = [n for n in z.namelist() if "LICENSE" in n]
            assert len(license_files) >= 1

    def test_sdist_contents(self):
        """sdist 必须包含源码"""
        with tarfile.open(self.sdist, "r:gz") as t:
            names = t.getnames()
            # sdist 应该包含 pyproject.toml 和源码
            assert any("pyproject.toml" in n for n in names)
            assert any("__init__.py" in n for n in names)

    def test_publish_workflow_exists(self):
        """publish.yml 必须存在"""
        wf = Path(__file__).parent.parent / ".github" / "workflows" / "publish.yml"
        assert wf.exists()

    def test_publish_workflow_uses_trusted_publishing(self):
        """publish.yml 必须使用 OIDC trusted publishing"""
        wf = Path(__file__).parent.parent / ".github" / "workflows" / "publish.yml"
        content = wf.read_text()
        assert "id-token: write" in content
        assert "pypa/gh-action-pypi-publish" in content