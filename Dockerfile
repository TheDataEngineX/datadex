ARG SERVICE_PACKAGE=datadex
ARG SERVICE_PORT=17001

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/
RUN uv sync --frozen --no-dev

FROM python:3.13-slim
ARG SERVICE_PACKAGE
ARG SERVICE_PORT

COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    SERVICE_PACKAGE=${SERVICE_PACKAGE} \
    SERVICE_PORT=${SERVICE_PORT}

EXPOSE ${SERVICE_PORT}
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${SERVICE_PORT}/health')"

USER 1000
CMD ["sh", "-c", "exec uvicorn ${SERVICE_PACKAGE}.api.main:app --host 0.0.0.0 --port ${SERVICE_PORT}"]
