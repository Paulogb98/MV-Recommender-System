# Backend production build. Build context is the repo root (see docker-compose.yml)
# because the backend needs to copy ml/artifacts/, which lives outside backend/,
# and the dependency manifest (pyproject.toml/uv.lock) lives at the repo root too.
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY backend/app ./app
COPY ml/artifacts ./ml/artifacts

# Overrides the app/core/config.py default (computed via __file__, only correct
# in local dev), since the folder structure inside the container is shallower.
ENV ARTIFACTS_DIR=/app/ml/artifacts
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
