# HTZL A Share MCP - Production Docker Image
FROM python:3.12-slim

WORKDIR /app

# 系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python 依赖（先装依赖层缓存）
COPY pyproject.toml ./
RUN pip install --no-cache-dir hatchling fastmcp akshare pandas numpy requests \
    pysnowball redis pybloomfiltermmap3 anthropic talib-binary

# 源码
COPY src/ ./src/
RUN pip install --no-cache-dir -e .

# 环境变量默认值
ENV HTZL_USE_MOCK=true
ENV TRANSPORT=streamable-http
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 启动命令
CMD ["sh", "-c", "python -m htzl_a_share_mcp.server --transport ${TRANSPORT} --host ${HOST} --port ${PORT}"]