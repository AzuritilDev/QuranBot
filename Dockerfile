FROM python:3.12-slim AS builder

# Copy uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and use 'copy' mode for better performance
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1. Install dependencies separately to leverage Docker layer caching
# This layer only rebuilds if uv.lock or pyproject.toml changes
COPY uv.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 2. Copy the rest of the source code and sync the project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage 2: Final runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure the virtual environment is used
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "main.py", "t"]