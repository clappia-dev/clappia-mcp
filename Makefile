# Clappia MCP Server Makefile
# ===========================

# Configuration
PROJECT_NAME = clappia-mcp
DOCKER_IMAGE = okaru413/clappia-mcp
VERSION ?= 1.0.0
DOCKER_HUB_USERNAME ?= $(shell echo $$DOCKER_HUB_USERNAME)

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

# Docker Commands
.PHONY: docker-build
docker-build: ## Build main Docker image
	@echo "$(BLUE)Building main Docker image: $(DOCKER_IMAGE):$(VERSION)$(NC)"
	docker build -t $(DOCKER_IMAGE):$(VERSION) .
	docker build -t $(DOCKER_IMAGE):latest .
	@echo "$(GREEN)✅ Main Docker image built successfully$(NC)"

# Individual Docker Build Commands
.PHONY: docker-build-form
docker-build-form: ## Build Docker image for form server
	@echo "$(BLUE)Building Docker image for form server...$(NC)"
	docker build -f Dockerfile.form -t $(DOCKER_IMAGE)-form:$(VERSION) .
	docker build -f Dockerfile.form -t $(DOCKER_IMAGE)-form:latest .
	@echo "$(GREEN)✅ Form Docker image built successfully$(NC)"

.PHONY: docker-build-workflow
docker-build-workflow: ## Build Docker image for workflow server
	@echo "$(BLUE)Building Docker image for workflow server...$(NC)"
	docker build -f Dockerfile.workflow -t $(DOCKER_IMAGE)-workflow:$(VERSION) .
	docker build -f Dockerfile.workflow -t $(DOCKER_IMAGE)-workflow:latest .
	@echo "$(GREEN)✅ Workflow Docker image built successfully$(NC)"

.PHONY: docker-build-submission
docker-build-submission: ## Build Docker image for submission server
	@echo "$(BLUE)Building Docker image for submission server...$(NC)"
	docker build -f Dockerfile.submission -t $(DOCKER_IMAGE)-submission:$(VERSION) .
	docker build -f Dockerfile.submission -t $(DOCKER_IMAGE)-submission:latest .
	@echo "$(GREEN)✅ Submission Docker image built successfully$(NC)"

.PHONY: docker-build-workplace
docker-build-workplace: ## Build Docker image for workplace server
	@echo "$(BLUE)Building Docker image for workplace server...$(NC)"
	docker build -f Dockerfile.workplace -t $(DOCKER_IMAGE)-workplace:$(VERSION) .
	docker build -f Dockerfile.workplace -t $(DOCKER_IMAGE)-workplace:latest .
	@echo "$(GREEN)✅ Workplace Docker image built successfully$(NC)"

.PHONY: docker-build-charts
docker-build-charts: ## Build Docker image for charts server
	@echo "$(BLUE)Building Docker image for charts server...$(NC)"
	docker build -f Dockerfile.charts -t $(DOCKER_IMAGE)-charts:$(VERSION) .
	docker build -f Dockerfile.charts -t $(DOCKER_IMAGE)-charts:latest .
	@echo "$(GREEN)✅ Charts Docker image built successfully$(NC)"

.PHONY: docker-build-all
docker-build-all: docker-build docker-build-form docker-build-workflow docker-build-submission docker-build-workplace docker-build-charts ## Build all Docker images
	@echo "$(GREEN)🎉 All Docker images built successfully$(NC)"

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
docker-push: ## Push main Docker image to registry (usage: make docker-push DOCKER_HUB_USERNAME=yourusername)
	@echo "$(BLUE)Pushing main Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		echo "Usage: make docker-push DOCKER_HUB_USERNAME=yourusername"; \
		exit 1; \
	fi
	docker login
	docker push $(DOCKER_IMAGE):$(VERSION)
	docker push $(DOCKER_IMAGE):latest
	@echo "$(GREEN)✅ Main Docker image pushed successfully$(NC)"

# Individual Docker Push Commands
.PHONY: docker-push-form
docker-push-form: ## Push form Docker image to registry
	@echo "$(BLUE)Pushing form Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker push $(DOCKER_IMAGE)-form:$(VERSION)
	docker push $(DOCKER_IMAGE)-form:latest
	@echo "$(GREEN)✅ Form Docker image pushed successfully$(NC)"

.PHONY: docker-push-workflow
docker-push-workflow: ## Push workflow Docker image to registry
	@echo "$(BLUE)Pushing workflow Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker push $(DOCKER_IMAGE)-workflow:$(VERSION)
	docker push $(DOCKER_IMAGE)-workflow:latest
	@echo "$(GREEN)✅ Workflow Docker image pushed successfully$(NC)"

.PHONY: docker-push-submission
docker-push-submission: ## Push submission Docker image to registry
	@echo "$(BLUE)Pushing submission Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker push $(DOCKER_IMAGE)-submission:$(VERSION)
	docker push $(DOCKER_IMAGE)-submission:latest
	@echo "$(GREEN)✅ Submission Docker image pushed successfully$(NC)"

.PHONY: docker-push-workplace
docker-push-workplace: ## Push workplace Docker image to registry
	@echo "$(BLUE)Pushing workplace Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker push $(DOCKER_IMAGE)-workplace:$(VERSION)
	docker push $(DOCKER_IMAGE)-workplace:latest
	@echo "$(GREEN)✅ Workplace Docker image pushed successfully$(NC)"

.PHONY: docker-push-charts
docker-push-charts: ## Push charts Docker image to registry
	@echo "$(BLUE)Pushing charts Docker image to registry...$(NC)"
	@if [ -z "$(DOCKER_HUB_USERNAME)" ]; then \
		echo "$(YELLOW)⚠️  DOCKER_HUB_USERNAME not set$(NC)"; \
		exit 1; \
	fi
	docker push $(DOCKER_IMAGE)-charts:$(VERSION)
	docker push $(DOCKER_IMAGE)-charts:latest
	@echo "$(GREEN)✅ Charts Docker image pushed successfully$(NC)"

.PHONY: docker-push-all
docker-push-all: docker-push docker-push-form docker-push-workflow docker-push-submission docker-push-workplace docker-push-charts ## Push all Docker images to registry
	@echo "$(GREEN)🎉 All Docker images pushed successfully$(NC)"

# Deployment Pipeline
.PHONY: deploy
deploy: clean install docker-build docker-push ## Full deployment pipeline (usage: make deploy DOCKER_HUB_USERNAME=yourusername)
	@echo "$(GREEN)🎉 Full deployment completed!$(NC)"

# Utility Commands
.PHONY: status
status: ## Show project status
	@echo "$(BLUE)Project Status$(NC)"
	@echo "=============="
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Docker Image: $(DOCKER_IMAGE)"
	@echo ""
	@echo "$(BLUE)Environment$(NC)"
	@echo "CLAPPIA_API_KEY: $${CLAPPIA_API_KEY:+✅ Set} $${CLAPPIA_API_KEY:-❌ Not Set}"
	@echo "DOCKER_HUB_USERNAME: $${DOCKER_HUB_USERNAME:+✅ Set} $${DOCKER_HUB_USERNAME:-❌ Not Set}"

.PHONY: setup
setup: install ## Initial project setup
	@echo "$(GREEN)✅ Project setup completed!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Set your API key: export CLAPPIA_API_KEY=your_key_here"
	@echo "2. Test locally: make run"
	@echo "3. Deploy: make deploy DOCKER_HUB_USERNAME=yourusername"