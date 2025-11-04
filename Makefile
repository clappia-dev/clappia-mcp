# Clappia MCP Server Makefile
# ===========================

# Configuration
PROJECT_NAME = clappia-mcp
DOCKER_IMAGE = okaru413/clappia-mcp
VERSION ?= 1.0.0
DOCKER_HUB_USERNAME ?= $(shell echo $$DOCKER_HUB_USERNAME)
PLATFORMS = linux/amd64,linux/arm64

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# No default target - require explicit command
.DEFAULT_GOAL := error

# Error target - show when no command specified
.PHONY: error
error:
	@echo "$(YELLOW)❌ No command specified!$(NC)"
	@echo ""
	@echo "$(BLUE)Available Commands:$(NC)"
	@echo "======================"
	@echo ""
	@echo "$(GREEN)Server Commands:$(NC)"
	@echo "  make run-auth             # Run auth server on port 9000"
	@echo "  make run-http             # Run HTTP server on port 3000"
	@echo ""
	@echo "$(GREEN)Tunnel Commands:$(NC)"
	@echo "  make tunnel-auth           # Forward auth server with localtunnel"
	@echo "  make tunnel-http           # Forward HTTP server with localtunnel"
	@echo "  make tunnel-both           # Show instructions for both tunnels"
	@echo "  make run-auth-tunnel       # Run auth server + tunnel together"
	@echo "  make run-http-tunnel       # Run HTTP server + tunnel together"
	@echo ""
	@echo "$(GREEN)Build Commands:$(NC)"
	@echo "  make docker-build-http    # Build HTTP/SSE server (multi-platform)"
	@echo "  make docker-build-http-amd64 # Build HTTP/SSE server (AMD64 only)"
	@echo "  make docker-build-http-arm64 # Build HTTP/SSE server (ARM64 only)"
	@echo "  make docker-build-mcp      # Build MCP server"
	@echo "  make docker-build-all      # Build all servers (HTTP and MCP)"
	@echo ""
	@echo "$(GREEN)Other Commands:$(NC)"
	@echo "  make help                  # Show full help"
	@echo "  make status               # Show project status"
	@echo "  make setup                # Initial setup"
	@echo ""
	@echo "$(YELLOW)Example: make docker-build-http$(NC)"
	@exit 1

# Help target
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Clappia MCP Server - Available Commands$(NC)"
	@echo "=========================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Commands
.PHONY: install
install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: clean
clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf .venv __pycache__ tools/__pycache__ utils/__pycache__ .pytest_cache dist/ build/ *.egg-info/
	@echo "$(GREEN)✅ Cleaned build artifacts$(NC)"

.PHONY: run
run: ## Run the main MCP server locally
	@echo "$(BLUE)Running main MCP server locally...$(NC)"
	uv run main_server.py

# Individual Server Commands
.PHONY: run-auth
run-auth: ## Run auth server on port 9000
	@echo "$(BLUE)Running Auth server on port 9000...$(NC)"
	uv run auth_server.py

.PHONY: run-http
run-http: ## Run HTTP server on port 3000
	@echo "$(BLUE)Running HTTP server on port 3000...$(NC)"
	uv run http_server.py

.PHONY: tunnel-auth
tunnel-auth: ## Forward auth server (port 9000) with localtunnel
	@echo "$(BLUE)Forwarding auth server (port 9000) with localtunnel...$(NC)"
	@echo "$(YELLOW)Make sure auth server is running first: make run-auth$(NC)"
	lt --port 9000 --subdomain clappia-auth

.PHONY: tunnel-http
tunnel-http: ## Forward HTTP server (port 3000) with localtunnel
	@echo "$(BLUE)Forwarding HTTP server (port 3000) with localtunnel...$(NC)"
	@echo "$(YELLOW)Make sure HTTP server is running first: make run-http$(NC)"
	lt --port 3000 --subdomain clappia-mcp

.PHONY: tunnel-both
tunnel-both: ## Forward both servers with localtunnel (run in separate terminals)
	@echo "$(BLUE)Forwarding both servers with localtunnel...$(NC)"
	@echo "$(YELLOW)Run these commands in separate terminals:$(NC)"
	@echo "Terminal 1: make tunnel-auth"
	@echo "Terminal 2: make tunnel-http"
	@echo ""
	@echo "$(GREEN)Or run servers and tunnels together:$(NC)"
	@echo "Terminal 1: make run-auth-tunnel"
	@echo "Terminal 2: make run-http-tunnel"

.PHONY: run-auth-tunnel
run-auth-tunnel: ## Run auth server and tunnel together
	@echo "$(BLUE)Running auth server and tunnel together...$(NC)"
	@echo "$(YELLOW)Starting auth server in background...$(NC)"
	uv run auth_server.py &
	AUTH_PID=$$!; \
	echo "Auth server PID: $$AUTH_PID"; \
	sleep 3; \
	echo "$(YELLOW)Starting tunnel...$(NC)"; \
	lt --port 9000 --subdomain clappia-auth; \
	kill $$AUTH_PID 2>/dev/null || true

.PHONY: run-http-tunnel
run-http-tunnel: ## Run HTTP server and tunnel together
	@echo "$(BLUE)Running HTTP server and tunnel together...$(NC)"
	@echo "$(YELLOW)Starting HTTP server in background...$(NC)"
	uv run http_server.py &
	HTTP_PID=$$!; \
	echo "HTTP server PID: $$HTTP_PID"; \
	sleep 3; \
	echo "$(YELLOW)Starting tunnel...$(NC)"; \
	lt --port 3000 --subdomain clappia-mcp; \
	kill $$HTTP_PID 2>/dev/null || true

# Docker Setup
.PHONY: docker-setup
docker-setup: ## Setup Docker buildx for multi-platform builds
	@echo "$(BLUE)Setting up Docker buildx for multi-platform builds...$(NC)"
	docker buildx create --name multiarch-builder --use 2>/dev/null || docker buildx use multiarch-builder
	@echo "$(GREEN)✅ Docker buildx setup completed$(NC)"

# Multi-Platform Docker Commands
.PHONY: docker-build-http
docker-build-http: docker-setup ## Build multi-platform HTTP/SSE Docker image with rich metadata
	@echo "$(BLUE)Building multi-platform HTTP/SSE Docker image: $(DOCKER_IMAGE):$(VERSION) for $(PLATFORMS)$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--load \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ Multi-platform HTTP/SSE Docker image built successfully$(NC)"

.PHONY: docker-build-all
docker-build-all: docker-build-http docker-build-mcp ## Build all multi-platform Docker images (HTTP and MCP)
	@echo "$(GREEN)🎉 All multi-platform Docker images built successfully$(NC)"

# Legacy single-platform builds (for compatibility)
.PHONY: docker-build-single
docker-build-single: ## Build single-platform Docker image (current architecture only)
	@echo "$(BLUE)Building single-platform Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker build -t $(DOCKER_IMAGE):$(VERSION) -f Dockerfile.http .
	docker tag $(DOCKER_IMAGE):$(VERSION) $(DOCKER_IMAGE):latest
	@echo "$(GREEN)✅ Single-platform Docker image built successfully$(NC)"

# Platform-specific builds to avoid warnings
.PHONY: docker-build-http-amd64
docker-build-http-amd64: ## Build HTTP/SSE Docker image for AMD64 platform only
	@echo "$(BLUE)Building AMD64 HTTP/SSE Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker buildx build \
		--platform linux/amd64 \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--load \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ AMD64 HTTP/SSE Docker image built successfully$(NC)"

.PHONY: docker-build-http-arm64
docker-build-http-arm64: ## Build HTTP/SSE Docker image for ARM64 platform only
	@echo "$(BLUE)Building ARM64 HTTP/SSE Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker buildx build \
		--platform linux/arm64 \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--load \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ ARM64 HTTP/SSE Docker image built successfully$(NC)"

# Simple Docker build using MCP Dockerfile
.PHONY: docker-build-mcp
docker-build-mcp: ## Build Docker image using MCP Dockerfile (fast local build)
	@echo "$(BLUE)Building Docker image using MCP Dockerfile: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker build \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		-f Dockerfile.mcp .
	@echo "$(GREEN)✅ Docker image built successfully using MCP Dockerfile$(NC)"


.PHONY: docker-run
docker-run: ## Run Docker container with main server
	@echo "$(BLUE)Running Docker container with main server...$(NC)"
	docker run --rm -it \
		$(DOCKER_IMAGE):latest

.PHONY: docker-push
docker-push: docker-setup ## Push multi-platform HTTP/SSE Docker image to registry
	@echo "$(BLUE)Pushing multi-platform HTTP/SSE Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		echo "Usage: make docker-push DOCKER_HUB_USERNAME=yourusername"; \
		exit 1; \
	fi
	docker login
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--push \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ Multi-platform HTTP/SSE Docker image pushed successfully$(NC)"

.PHONY: docker-push-all
docker-push-all: docker-push ## Push all multi-platform Docker images to registry (HTTP and MCP)
	@echo "$(GREEN)🎉 All multi-platform Docker images pushed successfully$(NC)"

# Deployment Pipeline
.PHONY: deploy
deploy: clean install docker-build-http docker-push ## Full deployment pipeline with multi-platform support
	@echo "$(GREEN)🎉 Full multi-platform deployment completed!$(NC)"

# Utility Commands
.PHONY: status
status: ## Show project status
	@echo "$(BLUE)Project Status$(NC)"
	@echo "=============="
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Docker Image: $(DOCKER_IMAGE)"
	@echo "Platforms: $(PLATFORMS)"
	@echo ""
	@echo "$(BLUE)Environment$(NC)"
	@echo "DOCKER_HUB_USERNAME: $${DOCKER_HUB_USERNAME:+✅ Set} $${DOCKER_HUB_USERNAME:-❌ Not Set}"
	@echo ""
	@echo "$(BLUE)Docker Buildx Status$(NC)"
	@docker buildx ls 2>/dev/null || echo "❌ Docker buildx not available"

.PHONY: setup
setup: install docker-setup ## Initial project setup with multi-platform support
	@echo "$(GREEN)✅ Project setup with multi-platform support completed!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Test locally: make run"
	@echo "2. Build multi-platform: make docker-build"
	@echo "3. Deploy: make deploy DOCKER_HUB_USERNAME=yourusername"

# Inspection Commands
.PHONY: docker-inspect
docker-inspect: ## Inspect multi-platform image details
	@echo "$(BLUE)Inspecting multi-platform image: $(DOCKER_IMAGE):latest$(NC)"
	docker buildx imagetools inspect $(DOCKER_IMAGE):latest 2>/dev/null || \
	docker image inspect $(DOCKER_IMAGE):latest --format 'Architecture: {{.Architecture}}, OS: {{.Os}}'

.PHONY: docker-inspect-all
docker-inspect-all: ## Inspect all multi-platform images
	@echo "$(BLUE)Inspecting all multi-platform images...$(NC)"
	@for image in "$(DOCKER_IMAGE)"; do \
		echo ""; \
		echo "Image: $$image:latest"; \
		docker buildx imagetools inspect $$image:latest 2>/dev/null | grep "Platform:" || \
		docker image inspect $$image:latest --format 'Single platform: {{.Os}}/{{.Architecture}}' 2>/dev/null || \
		echo "❌ Image not found"; \
	done