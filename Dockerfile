FROM python:3.13-slim

LABEL org.opencontainers.image.title="Clappia MCP Server (HTTP/SSE)"
LABEL org.opencontainers.image.description="Model Context Protocol (MCP) server for Clappia integration with HTTP/SSE transport. Enables AI assistants to interact with Clappia workspaces, forms, workflows, and analytics through a standardized protocol with web-based transport."
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Clappia Development Team <dev@clappia.com>"
LABEL org.opencontainers.image.vendor="Clappia"
LABEL org.opencontainers.image.url="https://github.com/clappia-dev/clappia-mcp"
LABEL org.opencontainers.image.documentation="https://github.com/clappia-dev/clappia-mcp/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/clappia-dev/clappia-mcp"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.created="2025-01-01T00:00:00Z"
LABEL org.opencontainers.image.revision="main"

LABEL io.modelcontextprotocol.server.name="io.github.clappia-dev/clappia-mcp-http"
LABEL io.modelcontextprotocol.server.version="1.0.0"
LABEL clappia.server.type="http-sse"
LABEL clappia.server.features="workspace,forms,workflows,submissions,analytics"
LABEL clappia.server.transport="http,sse"

LABEL maintainer="Clappia Development Team <dev@clappia.com>"
LABEL summary="MCP server with HTTP/SSE transport for Clappia integration"
LABEL description="This Docker image provides a Model Context Protocol (MCP) server with HTTP/SSE transport that enables AI assistants to interact with Clappia's no-code platform. Features include workspace management, form definitions, workflow automation, submission handling, and analytics access through web-based transport."

LABEL org.opencontainers.image.platform="linux/amd64,linux/arm64"
LABEL architecture="multi-platform"
LABEL compatibility="Intel x86_64, Apple Silicon ARM64"

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

LABEL org.opencontainers.image.platform.detected="${TARGETPLATFORM}"
LABEL org.opencontainers.image.platform.build="${BUILDPLATFORM}"

LABEL usage="docker run -p 8080:8080 -e ENVIRONMENT=dev -e WORKERS=2 clappia-mcp:latest"
LABEL environment.ENVIRONMENT="Optional: Environment selection (dev/qa/prod). Default: dev"
LABEL environment.WORKERS="Optional: Number of worker processes. Default: 2"
LABEL ports.exposed="8080 (HTTP/SSE endpoint)"
LABEL volumes.recommended="None required"

LABEL keywords="clappia,mcp,model-context-protocol,ai,no-code,workflow,forms,automation,claude,openai,http,sse,web,async"
LABEL category="Development Tools, AI/ML, Automation, Web Services"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV ENVIRONMENT=dev
ENV WORKERS=2

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN echo "Building for platform: ${TARGETPLATFORM:-unknown}" && \
    echo "Build platform: ${BUILDPLATFORM:-unknown}"

RUN uv sync

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

EXPOSE $PORT

CMD ["uv", "run", "http_server.py"]

LABEL readme.overview="Clappia MCP Server with HTTP/SSE transport enables AI assistants to seamlessly integrate with Clappia's no-code platform through web-based communication."
LABEL readme.features="• Multi-platform support (Intel & Apple Silicon)\n• Async HTTP server with multiple workers\n• HTTP/SSE transport for web integration\n• Workspace management\n• Form definitions and structure access\n• Workflow automation\n• Submission data handling\n• Analytics and reporting\n• OAuth 2.0 authentication\n• Health check endpoint"
LABEL readme.requirements="• Docker installed\n• Network access to Clappia services\n• Port available (default: 8080, configurable via PORT env var)"
LABEL readme.quickstart="1. docker run -p 8080:8080 -e PORT=8080 -e ENVIRONMENT=dev -e WORKERS=2 clappia-mcp:latest\n2. Access health endpoint: curl http://localhost:8080/health\n3. Scale workers: docker run -p 8080:8080 -e PORT=8080 -e ENVIRONMENT=dev -e WORKERS=4 clappia-mcp:latest"
LABEL readme.endpoints="• Health: GET /health\n• OAuth Metadata: GET /.well-known/oauth-protected-resource\n• MCP SSE: /sse (requires OAuth token)\n• Authentication: Bearer token via Authorization header"
LABEL readme.configuration="Environment Variables:\n• PORT: Server port (default: 8080)\n• ENVIRONMENT: dev/qa/prod (default: dev)\n• WORKERS: Number of worker processes (default: 2)"

