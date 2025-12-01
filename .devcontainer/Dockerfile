FROM ghcr.io/astral-sh/uv:latest AS uv

FROM ghcr.io/sondreomar/splunk-devcontainer:10

ENV UV_LINK_MODE=copy

COPY --from=uv --chown=splunk: /uv /uvx /bin/
