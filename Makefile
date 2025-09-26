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

# Default target
.DEFAULT_GOAL := help

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
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run main_server.py

# Individual Server Commands
.PHONY: run-form
run-form: ## Run clappia-app-form server
	@echo "$(BLUE)Running Clappia App Form server...$(NC)"
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run definitions_server.py

.PHONY: run-workflow
run-workflow: ## Run clappia-app-workflow server
	@echo "$(BLUE)Running Clappia App Workflow server...$(NC)"
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run workflows_server.py

.PHONY: run-submission
run-submission: ## Run clappia-app-submission server
	@echo "$(BLUE)Running Clappia App Submission server...$(NC)"
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run submissions_server.py

.PHONY: run-workplace
run-workplace: ## Run clappia-workplace server
	@echo "$(BLUE)Running Clappia Workplace server...$(NC)"
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run workplace_server.py

.PHONY: run-charts
run-charts: ## Run clappia-app-charts server
	@echo "$(BLUE)Running Clappia App Charts server...$(NC)"
	@if [ -z "$$CLAPPIA_API_KEY" ]; then \
		echo "$(YELLOW)⚠️  CLAPPIA_API_KEY not set$(NC)"; \
		echo "Please set your API key: export CLAPPIA_API_KEY=your_key_here"; \
		exit 1; \
	fi
	uv run analytics_server.py

# Docker Setup
.PHONY: docker-setup
docker-setup: ## Setup Docker buildx for multi-platform builds
	@echo "$(BLUE)Setting up Docker buildx for multi-platform builds...$(NC)"
	docker buildx create --name multiarch-builder --use 2>/dev/null || docker buildx use multiarch-builder
	@echo "$(GREEN)✅ Docker buildx setup completed$(NC)"

# Multi-Platform Docker Commands
.PHONY: docker-build
docker-build: docker-setup ## Build multi-platform Docker image with rich metadata
	@echo "$(BLUE)Building multi-platform Docker image: $(DOCKER_IMAGE):$(VERSION) for $(PLATFORMS)$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Docker image built successfully$(NC)"

# Individual Multi-Platform Docker Build Commands
.PHONY: docker-build-form
docker-build-form: docker-setup ## Build multi-platform Docker image for form server
	@echo "$(BLUE)Building multi-platform Docker image for form server...$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.form \
		-t $(DOCKER_IMAGE)-form:$(VERSION) \
		-t $(DOCKER_IMAGE)-form:latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Form Docker image built successfully$(NC)"

.PHONY: docker-build-workflow
docker-build-workflow: docker-setup ## Build multi-platform Docker image for workflow server
	@echo "$(BLUE)Building multi-platform Docker image for workflow server...$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.workflow \
		-t $(DOCKER_IMAGE)-workflow:$(VERSION) \
		-t $(DOCKER_IMAGE)-workflow:latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Workflow Docker image built successfully$(NC)"

.PHONY: docker-build-submission
docker-build-submission: docker-setup ## Build multi-platform Docker image for submission server
	@echo "$(BLUE)Building multi-platform Docker image for submission server...$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.submission \
		-t $(DOCKER_IMAGE)-submission:$(VERSION) \
		-t $(DOCKER_IMAGE)-submission:latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Submission Docker image built successfully$(NC)"

.PHONY: docker-build-workplace
docker-build-workplace: docker-setup ## Build multi-platform Docker image for workplace server
	@echo "$(BLUE)Building multi-platform Docker image for workplace server...$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.workplace \
		-t $(DOCKER_IMAGE)-workplace:$(VERSION) \
		-t $(DOCKER_IMAGE)-workplace:latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Workplace Docker image built successfully$(NC)"

.PHONY: docker-build-charts
docker-build-charts: docker-setup ## Build multi-platform Docker image for charts server
	@echo "$(BLUE)Building multi-platform Docker image for charts server...$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.charts \
		-t $(DOCKER_IMAGE)-charts:$(VERSION) \
		-t $(DOCKER_IMAGE)-charts:latest \
		--load \
		.
	@echo "$(GREEN)✅ Multi-platform Charts Docker image built successfully$(NC)"

.PHONY: docker-build-all
docker-build-all: docker-build docker-build-form docker-build-workflow docker-build-submission docker-build-workplace docker-build-charts ## Build all multi-platform Docker images
	@echo "$(GREEN)🎉 All multi-platform Docker images built successfully$(NC)"

# Legacy single-platform builds (for compatibility)
.PHONY: docker-build-single
docker-build-single: ## Build single-platform Docker image (current architecture only)
	@echo "$(BLUE)Building single-platform Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker build -t $(DOCKER_IMAGE):$(VERSION) .
	docker build -t $(DOCKER_IMAGE):latest .
	@echo "$(GREEN)✅ Single-platform Docker image built successfully$(NC)"

.PHONY: docker-run
docker-run: ## Run Docker container with main server
	@echo "$(BLUE)Running Docker container with main server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE):latest

.PHONY: docker-run-form
docker-run-form: ## Run Docker container with form server
	@echo "$(BLUE)Running Docker container with form server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE)-form:latest

.PHONY: docker-run-workflow
docker-run-workflow: ## Run Docker container with workflow server
	@echo "$(BLUE)Running Docker container with workflow server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE)-workflow:latest

.PHONY: docker-run-submission
docker-run-submission: ## Run Docker container with submission server
	@echo "$(BLUE)Running Docker container with submission server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE)-submission:latest

.PHONY: docker-run-workplace
docker-run-workplace: ## Run Docker container with workplace server
	@echo "$(BLUE)Running Docker container with workplace server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE)-workplace:latest

.PHONY: docker-run-charts
docker-run-charts: ## Run Docker container with charts server
	@echo "$(BLUE)Running Docker container with charts server...$(NC)"
	docker run --rm -it \
		-e CLAPPIA_API_KEY=$${CLAPPIA_API_KEY} \
		$(DOCKER_IMAGE)-charts:latest

.PHONY: docker-push
docker-push: docker-setup ## Push multi-platform Docker image to registry
	@echo "$(BLUE)Pushing multi-platform Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		echo "Usage: make docker-push DOCKER_HUB_USERNAME=yourusername"; \
		exit 1; \
	fi
	docker login
	docker buildx build \
		--platform $(PLATFORMS) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Docker image pushed successfully$(NC)"

# Individual Docker Push Commands
.PHONY: docker-push-form
docker-push-form: docker-setup ## Push multi-platform form Docker image to registry
	@echo "$(BLUE)Pushing multi-platform form Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.form \
		-t $(DOCKER_IMAGE)-form:$(VERSION) \
		-t $(DOCKER_IMAGE)-form:latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Form Docker image pushed successfully$(NC)"

.PHONY: docker-push-workflow
docker-push-workflow: docker-setup ## Push multi-platform workflow Docker image to registry
	@echo "$(BLUE)Pushing multi-platform workflow Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.workflow \
		-t $(DOCKER_IMAGE)-workflow:$(VERSION) \
		-t $(DOCKER_IMAGE)-workflow:latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Workflow Docker image pushed successfully$(NC)"

.PHONY: docker-push-submission
docker-push-submission: docker-setup ## Push multi-platform submission Docker image to registry
	@echo "$(BLUE)Pushing multi-platform submission Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.submission \
		-t $(DOCKER_IMAGE)-submission:$(VERSION) \
		-t $(DOCKER_IMAGE)-submission:latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Submission Docker image pushed successfully$(NC)"

.PHONY: docker-push-workplace
docker-push-workplace: docker-setup ## Push multi-platform workplace Docker image to registry
	@echo "$(BLUE)Pushing multi-platform workplace Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.workplace \
		-t $(DOCKER_IMAGE)-workplace:$(VERSION) \
		-t $(DOCKER_IMAGE)-workplace:latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Workplace Docker image pushed successfully$(NC)"

.PHONY: docker-push-charts
docker-push-charts: docker-setup ## Push multi-platform charts Docker image to registry
	@echo "$(BLUE)Pushing multi-platform charts Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker buildx build \
		--platform $(PLATFORMS) \
		-f Dockerfile.charts \
		-t $(DOCKER_IMAGE)-charts:$(VERSION) \
		-t $(DOCKER_IMAGE)-charts:latest \
		--push \
		.
	@echo "$(GREEN)✅ Multi-platform Charts Docker image pushed successfully$(NC)"

.PHONY: docker-push-all
docker-push-all: docker-push docker-push-form docker-push-workflow docker-push-submission docker-push-workplace docker-push-charts ## Push all multi-platform Docker images to registry
	@echo "$(GREEN)🎉 All multi-platform Docker images pushed successfully$(NC)"

# Deployment Pipeline
.PHONY: deploy
deploy: clean install docker-build docker-push ## Full deployment pipeline with multi-platform support
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
	@echo "CLAPPIA_API_KEY: $${CLAPPIA_API_KEY:+✅ Set} $${CLAPPIA_API_KEY:-❌ Not Set}"
	@echo "DOCKER_HUB_USERNAME: $${DOCKER_HUB_USERNAME:+✅ Set} $${DOCKER_HUB_USERNAME:-❌ Not Set}"
	@echo ""
	@echo "$(BLUE)Docker Buildx Status$(NC)"
	@docker buildx ls 2>/dev/null || echo "❌ Docker buildx not available"

.PHONY: setup
setup: install docker-setup ## Initial project setup with multi-platform support
	@echo "$(GREEN)✅ Project setup with multi-platform support completed!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Set your API key: export CLAPPIA_API_KEY=your_key_here"
	@echo "2. Test locally: make run"
	@echo "3. Build multi-platform: make docker-build"
	@echo "4. Deploy: make deploy DOCKER_HUB_USERNAME=yourusername"

# Inspection Commands
.PHONY: docker-inspect
docker-inspect: ## Inspect multi-platform image details
	@echo "$(BLUE)Inspecting multi-platform image: $(DOCKER_IMAGE):latest$(NC)"
	docker buildx imagetools inspect $(DOCKER_IMAGE):latest 2>/dev/null || \
	docker image inspect $(DOCKER_IMAGE):latest --format 'Architecture: {{.Architecture}}, OS: {{.Os}}'

.PHONY: docker-inspect-all
docker-inspect-all: ## Inspect all multi-platform images
	@echo "$(BLUE)Inspecting all multi-platform images...$(NC)"
	@for image in "$(DOCKER_IMAGE)" "$(DOCKER_IMAGE)-form" "$(DOCKER_IMAGE)-workflow" "$(DOCKER_IMAGE)-submission" "$(DOCKER_IMAGE)-workplace" "$(DOCKER_IMAGE)-charts"; do \
		echo ""; \
		echo "Image: $$image:latest"; \
		docker buildx imagetools inspect $$image:latest 2>/dev/null | grep "Platform:" || \
		docker image inspect $$image:latest --format 'Single platform: {{.Os}}/{{.Architecture}}' 2>/dev/null || \
		echo "❌ Image not found"; \
	done