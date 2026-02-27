FROM ghcr.io/astral-sh/uv:latest AS uv_builder

FROM python:3.13-slim

COPY --from=uv_builder /uv /usr/local/bin/

ENV UV_PROJECT_ENVIRONMENT=system

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]