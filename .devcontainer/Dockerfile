FROM ghcr.io/astral-sh/uv:latest AS uv

FROM ghcr.io/techcloud0/splunk-devcontainer:9.3

ENV UV_LINK_MODE=copy

COPY --from=uv --chown=splunk: /uv /uvx /bin/
