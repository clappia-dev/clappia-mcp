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

.PHONY: install
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: install-dev
install-dev:
	@echo "$(BLUE)Installing dependencies with dev tools...$(NC)"
	uv sync --extra dev
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

.PHONY: lint
lint:
	@echo "$(BLUE)Running linter...$(NC)"
	uv run ruff check .
	@echo "$(GREEN)✅ Linting completed$(NC)"

.PHONY: lint-fix
lint-fix:
	@echo "$(BLUE)Running linter with auto-fix...$(NC)"
	uv run ruff check --fix .
	@echo "$(GREEN)✅ Linting completed$(NC)"

.PHONY: format
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run ruff format .
	@echo "$(GREEN)✅ Formatting completed$(NC)"

.PHONY: format-check
format-check:
	@echo "$(BLUE)Checking code formatting...$(NC)"
	uv run ruff format --check .
	@echo "$(GREEN)✅ Format check completed$(NC)"

.PHONY: check
check: lint format-check
	@echo "$(GREEN)✅ All checks passed$(NC)"

.PHONY: clean
clean:
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf .venv __pycache__ src/**/__pycache__ .pytest_cache dist/ build/ *.egg-info/
	@echo "$(GREEN)✅ Cleaned build artifacts$(NC)"

.PHONY: build-http
build-http:
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
build-mcp:
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
push:
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
deploy: clean install build-http push
	@echo "$(GREEN)🎉 Deployment completed!$(NC)"

.PHONY: deploy-dev
deploy-dev:
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
deploy-qa:
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
deploy-prod:
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

