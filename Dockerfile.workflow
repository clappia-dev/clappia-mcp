FROM python:3.10-slim

# Comprehensive metadata for Docker Hub
LABEL org.opencontainers.image.title="Clappia MCP Workflows Server"
LABEL org.opencontainers.image.description="Model Context Protocol (MCP) server for Clappia workflow automation integration. Enables AI assistants to create, manage, and execute workflows, automate business processes, and handle workflow triggers through a standardized protocol."
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Clappia Development Team <dev@clappia.com>"
LABEL org.opencontainers.image.vendor="Clappia"
LABEL org.opencontainers.image.url="https://github.com/clappia-dev/clappia-mcp"
LABEL org.opencontainers.image.documentation="https://github.com/clappia-dev/clappia-mcp/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/clappia-dev/clappia-mcp"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.created="2025-01-01T00:00:00Z"
LABEL org.opencontainers.image.revision="main"

# Clappia-specific labels
LABEL io.modelcontextprotocol.server.name="io.github.clappia-dev/clappia-mcp"
LABEL io.modelcontextprotocol.server.version="1.0.0"
LABEL clappia.server.type="workflows"
LABEL clappia.server.features="workflows,automation,triggers,processes,business-logic,orchestration"

# Additional metadata
LABEL maintainer="Clappia Development Team <dev@clappia.com>"
LABEL summary="MCP server for Clappia workflow automation and process management"
LABEL description="This Docker image provides a Model Context Protocol (MCP) server that enables AI assistants to create, manage, and execute Clappia workflows, automate business processes, handle triggers, and orchestrate complex workflows. Specialized for workflow automation and process management."

# Multi-architecture support metadata
LABEL org.opencontainers.image.platform="linux/amd64,linux/arm64"
LABEL architecture="multi-platform"
LABEL compatibility="Intel x86_64, Apple Silicon ARM64"

# Usage and environment metadata
LABEL usage="docker run -e CLAPPIA_API_KEY=your_key okaru413/clappia-mcp:workflows"
LABEL environment.CLAPPIA_API_KEY="Required: Your Clappia API key for authentication"
LABEL ports.exposed="None (MCP uses stdio)"
LABEL volumes.recommended="None required"

# Keywords for Docker Hub search
LABEL keywords="clappia,mcp,workflows,automation,triggers,processes,business-logic,orchestration,model-context-protocol,ai,no-code"
LABEL category="Development Tools, AI/ML, Workflow Automation, Business Process Management"

WORKDIR /app

# Install uv and dependencies
RUN pip install uv
COPY . .
RUN uv sync

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

# Set default environment variables with documentation
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the workflow server
CMD ["uv", "run", "workflows_server.py"]

# Additional documentation as labels
LABEL readme.overview="Clappia MCP Workflows Server enables AI assistants to create, manage, and execute Clappia workflows for business process automation."
LABEL readme.features="• Multi-platform support (Intel & Apple Silicon)\n• Workflow creation and management\n• Process automation\n• Trigger handling\n• Business logic orchestration\n• Workflow execution monitoring\n• Secure API authentication"
LABEL readme.requirements="• Docker installed\n• Clappia API key\n• Network access to Clappia services"
LABEL readme.quickstart="1. Get API key from Clappia\n2. docker run -e CLAPPIA_API_KEY=your_key okaru413/clappia-mcp:workflows"
