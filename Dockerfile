# syntax=docker/dockerfile:1

# Python 3.15 final is not on Docker Hub yet; bump to 3.15 once it is.
ARG PYTHON_VERSION=3.15.0rc2

FROM python:${PYTHON_VERSION}-slim-trixie AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --locked --no-dev --no-install-project

FROM python:${PYTHON_VERSION}-slim-trixie AS runtime
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --no-create-home app
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY albo.py departments_regex.yaml ./
COPY utils/ utils/
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
USER app
# Expects settings.yaml and a writable data/ mounted at runtime (see compose.yaml).
CMD ["python", "albo.py"]
