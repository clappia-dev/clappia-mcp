# Clappia MCP Server Makefile
# ===========================

PROJECT_NAME = clappia-mcp
DOCKER_IMAGE = okaru413/clappia-mcp
VERSION ?= 1.0.0
DOCKER_HUB_USERNAME ?= $(shell echo $$DOCKER_HUB_USERNAME)
PLATFORMS = linux/amd64,linux/arm64

GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Installation
.PHONY: install
install: ## Install the package in production mode
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: install-dev
install-dev: ## Install the package with development dependencies
	@echo "$(BLUE)Installing dependencies with dev tools...$(NC)"
	uv sync --extra dev
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: install-hooks
install-hooks: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	uv run pre-commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed$(NC)"

# Code Formatting & Linting
.PHONY: format
format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run ruff format .
	uv run ruff check . --fix
	@echo "$(GREEN)✅ Formatting completed$(NC)"

.PHONY: lint
lint: ## Run linting and type checking
	@echo "$(BLUE)Running linter...$(NC)"
	uv run ruff check .
	@echo "$(BLUE)Running type checker...$(NC)"
	uv run mypy .
	@echo "$(GREEN)✅ Linting completed$(NC)"

.PHONY: check
check: format lint ## Run all checks (format first, then lint)
	@echo "$(GREEN)✅ All checks passed$(NC)"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks manually
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files
	@echo "$(GREEN)✅ Pre-commit checks completed$(NC)"

# Cleanup
.PHONY: clean
clean: ## Clean up build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/ dist/ *.egg-info/ .mypy_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Cleaned build artifacts$(NC)"

# Build
.PHONY: build
build: clean ## Build the package
	@echo "$(BLUE)Building package...$(NC)"
	uv build
	@echo "$(GREEN)✅ Package built successfully$(NC)"

# Lock Management
.PHONY: lock
lock: ## Generate/update lock file
	@echo "$(BLUE)Generating lock file...$(NC)"
	uv lock
	@echo "$(GREEN)✅ Lock file generated$(NC)"

.PHONY: sync
sync: ## Sync environment with lock file
	@echo "$(BLUE)Syncing environment...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Environment synced$(NC)"

# Docker & Deployment
.PHONY: build-http
build-http: ## Build multi-platform HTTP Docker image
	@echo "$(BLUE)Setting up Docker buildx...$(NC)"
	@docker buildx create --name multiarch-builder --use 2>/dev/null || docker buildx use multiarch-builder
	@echo "$(BLUE)Building multi-platform HTTP Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		--build-arg ENVIRONMENT=prod \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--load \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ HTTP Docker image built successfully$(NC)"

.PHONY: build-mcp
build-mcp: ## Build MCP Docker image
	@echo "$(BLUE)Building MCP Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker build \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		-f Dockerfile.mcp .
	@echo "$(GREEN)✅ MCP Docker image built successfully$(NC)"

.PHONY: push
push: ## Push Docker image to registry
	@echo "$(BLUE)Setting up Docker buildx...$(NC)"
	@docker buildx create --name multiarch-builder --use 2>/dev/null || docker buildx use multiarch-builder
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		echo "Usage: make push DOCKER_HUB_USERNAME=yourusername"; \
		exit 1; \
	fi
	@echo "$(BLUE)Pushing multi-platform HTTP Docker image...$(NC)"
	docker login
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
		--build-arg VERSION=$(VERSION) \
		--build-arg ENVIRONMENT=prod \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		--push \
		-f Dockerfile.http .
	@echo "$(GREEN)✅ Docker image pushed successfully$(NC)"

.PHONY: deploy
deploy: clean install build-http push ## Full deployment pipeline
	@echo "$(GREEN)🎉 Deployment completed!$(NC)"

.PHONY: deploy-dev
deploy-dev: ## Deploy to DEV environment
	@echo "$(BLUE)Setting up GCP project for DEV environment...$(NC)"
	gcloud config set project model-osprey-471909-q3
	@echo "$(BLUE)Compiling requirements.txt...$(NC)"
	uv pip compile pyproject.toml -o requirements.txt
	@echo "$(BLUE)Deploying to Google Cloud Run (DEV)...$(NC)"
	gcloud run deploy clappia-mcp-server \
		--source . \
		--platform managed \
		--region europe-west1 \
		--allow-unauthenticated \
		--memory 8Gi \
		--cpu 2 \
		--timeout 300 \
		--min-instances 0 \
		--max-instances 2 \
		--port 8080 \
		--set-env-vars ENVIRONMENT=dev \
		--clear-base-image
	@echo "$(GREEN)✅ GCP DEV deployment completed!$(NC)"

.PHONY: deploy-qa
deploy-qa: ## Deploy to QA environment
	@echo "$(BLUE)Setting up GCP project for QA environment...$(NC)"
	gcloud config set project model-osprey-471909-q3
	@echo "$(BLUE)Compiling requirements.txt...$(NC)"
	uv pip compile pyproject.toml -o requirements.txt
	@echo "$(BLUE)Deploying to Google Cloud Run (QA)...$(NC)"
	gcloud run deploy clappia-mcp-server-qa \
		--source . \
		--platform managed \
		--region europe-west1 \
		--allow-unauthenticated \
		--memory 8Gi \
		--cpu 2 \
		--timeout 300 \
		--min-instances 0 \
		--max-instances 2 \
		--port 8080 \
		--set-env-vars ENVIRONMENT=qa \
		--clear-base-image
	@echo "$(GREEN)✅ GCP QA deployment completed!$(NC)"

.PHONY: deploy-prod
deploy-prod: ## Deploy to PROD environment
	@echo "$(BLUE)Setting up GCP project for PROD environment...$(NC)"
	gcloud config set project model-osprey-471909-q3
	@echo "$(BLUE)Compiling requirements.txt...$(NC)"
	uv pip compile pyproject.toml -o requirements.txt
	@echo "$(BLUE)Deploying to Google Cloud Run (PROD)...$(NC)"
	gcloud run deploy clappia-mcp-server-prod \
		--source . \
		--platform managed \
		--region europe-west1 \
		--allow-unauthenticated \
		--memory 8Gi \
		--cpu 2 \
		--timeout 300 \
		--min-instances 0 \
		--max-instances 2 \
		--port 8080 \
		--set-env-vars ENVIRONMENT=prod \
		--clear-base-image
	@echo "$(GREEN)✅ GCP PROD deployment completed!$(NC)"

