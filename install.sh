#!/usr/bin/env bash
# install.sh — htzl-a-share-mcp 安装脚本
# 参考 zhoushoujianwork/easyeda-agent v1.0.2 (R835 起草)
# 适用平台: macOS / Linux
# 用法: curl -fsSL https://raw.githubusercontent.com/mm2xai/htzl-a-share-mcp-demo/main/install.sh | bash

set -euo pipefail

REPO="mm2xai/htzl-a-share-mcp-demo"
PACKAGE="htzl-a-share-mcp"
VERSION="${HTZL_A_SHARE_VERSION:-latest}"
INSTALL_DIR="${HTZL_A_SHARE_HOME:-$HOME/.htzl-a-share-mcp}"
BIN_DIR="${HTZL_A_SHARE_BIN:-$HOME/.local/bin}"

echo "==> htzl-a-share-mcp installer"
echo "    Repo:    $REPO"
echo "    Package: $PACKAGE"
echo "    Version: $VERSION"
echo "    Install: $INSTALL_DIR"
echo

# 1. 检查 Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 not found. Install Python 3.10+ first."
  exit 1
fi
PY_VERSION=$(python3 -c 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PY_VERSION detected"

# 2. 检查 / 创建 venv
if [ ! -d "$INSTALL_DIR/venv" ]; then
  echo "==> Creating venv at $INSTALL_DIR/venv"
  mkdir -p "$INSTALL_DIR"
  python3 -m venv "$INSTALL_DIR/venv"
fi
PY="$INSTALL_DIR/venv/bin/python"
PIP="$INSTALL_DIR/venv/bin/pip"

# 3. 升级 pip + 安装包
echo "==> Upgrading pip"
"$PY" -m pip install --upgrade pip --quiet
echo "==> Installing $PACKAGE @ $VERSION"
"$PIP" install "$PACKAGE${VERSION:+==$VERSION}" || "$PIP" install "git+https://github.com/$REPO.git"

# 4. 创建 bin wrapper
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/htzl-a-share-mcp" << WRAPPER
#!/usr/bin/env bash
# Wrapper for htzl-a-share-mcp MCP server
exec "$PY" -m htzl_a_share_mcp.server --transport "\${1:-stdio}"
WRAPPER
chmod +x "$BIN_DIR/htzl-a-share-mcp"
echo "✓ Installed: $BIN_DIR/htzl-a-share-mcp"

# 5. 健康检查
echo "==> Health check"
if "$PY" -c "import htzl_a_share_mcp; print('✓ module import OK:', htzl_a_share_mcp.__file__)" 2>&1; then
  echo "✓ Installation successful"
else
  echo "❌ Health check failed. Run: $PY -c 'import htzl_a_share_mcp'"
  exit 1
fi

echo
echo "🎉 htzl-a-share-mcp installed!"
echo
echo "Quick start:"
echo "  export PATH=\"$BIN_DIR:\$PATH\""
echo "  htzl-a-share-mcp stdio     # Run as MCP stdio server"
echo
echo "Add to OpenClaw (~/.openclaw/openclaw.json):"
cat << 'JSON'

{
  "mcp": {
    "servers": {
      "htzl-a-share": {
        "command": "$PY",
        "args": ["-m", "htzl_a_share_mcp.server", "--transport", "stdio"],
        "env": {"HTZL_USE_MOCK": "true"}
      }
    }
  }
}

JSON
