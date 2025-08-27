# Makefile for Kopi Challenge - Persuasive Debate Chatbot API
# ===============================================================
# 
# This Makefile provides all necessary commands for
# developing, testing and deploying the persuasive debate API.

.PHONY: help install test run dev down clean build lint format type-check coverage docker-build docker-clean logs status health

# Configuration variables
PROJECT_NAME := kopi-challenge
DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE_DEV_FILE := docker-compose.dev.yml
PYTHON_VERSION := 3.9
VENV_NAME := .venv

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target - show help
help: ## 📋 Show all available commands
	@echo ""
	@echo "$(BLUE)🤖 Kopi Challenge - Persuasive Debate Chatbot API$(NC)"
	@echo "$(BLUE)======================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Main commands (required by challenge):$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Usage examples:$(NC)"
	@echo "  make install    # Install all dependencies"
	@echo "  make run        # Start services in Docker"
	@echo "  make test       # Run all tests"
	@echo "  make down       # Stop all services"
	@echo "  make clean      # Clean containers and volumes"
	@echo ""

# Default command
default: help

# ================================
# MAIN COMMANDS (REQUIRED)
# ================================

install: ## 🔧 Install all dependencies and necessary tools
	@echo "$(BLUE)🔧 Installing dependencies...$(NC)"
	@$(MAKE) -s check-requirements
	@echo "$(GREEN)✅ Verifying and installing Python dependencies...$(NC)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "$(YELLOW)📦 Creating virtual environment...$(NC)"; \
		python$(PYTHON_VERSION) -m venv $(VENV_NAME) || python3 -m venv $(VENV_NAME); \
	fi
	@echo "$(YELLOW)📦 Activating virtual environment and installing packages...$(NC)"
	@. $(VENV_NAME)/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed successfully!$(NC)"
	@echo ""
	@echo "$(BLUE)🚀 To activate virtual environment manually:$(NC)"
	@echo "  source $(VENV_NAME)/bin/activate"
	@echo ""

test: ## 🧪 Run all tests (unit, integration, e2e)
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "$(RED)❌ Virtual environment not found. Run 'make install' first.$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)📋 Running unit tests...$(NC)"
	@. $(VENV_NAME)/bin/activate && python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Tests completed!$(NC)"
	@echo "$(BLUE)📊 Coverage report available at: htmlcov/index.html$(NC)"

run: ## 🚀 Start service and dependencies in Docker
	@echo "$(BLUE)🚀 Starting services in Docker...$(NC)"
	@$(MAKE) -s check-docker
	@echo "$(YELLOW)🐳 Building and starting containers...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d
	@echo "$(GREEN)✅ Services started successfully!$(NC)"
	@echo ""
	@$(MAKE) -s status
	@echo ""
	@echo "$(BLUE)🌐 API available at: http://localhost:8000$(NC)"
	@echo "$(BLUE)📚 Documentation at: http://localhost:8000/docs$(NC)"
	@echo "$(BLUE)❤️  Health check en: http://localhost:8000/health$(NC)"

down: ## ⏹️  Stop all services
	@echo "$(BLUE)⏹️  Stopping services...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down
	@docker-compose -f $(DOCKER_COMPOSE_DEV_FILE) down 2>/dev/null || true
	@echo "$(GREEN)✅ Services stopped successfully!$(NC)"

clean: ## 🧹 Clean and remove all containers, volumes and images
	@echo "$(BLUE)🧹 Cleaning Docker resources...$(NC)"
	@echo "$(YELLOW)⚠️  This will delete ALL containers, volumes and images from the project.$(NC)"
	@read -p "Are you sure? (y/N) " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(YELLOW)🗑️  Stopping containers...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down --remove-orphans 2>/dev/null || true
	@docker-compose -f $(DOCKER_COMPOSE_DEV_FILE) down --remove-orphans 2>/dev/null || true
	@echo "$(YELLOW)🗑️  Removing containers...$(NC)"
	@docker container prune -f
	@echo "$(YELLOW)🗑️  Removing project images...$(NC)"
	@docker images | grep "$(PROJECT_NAME)" | awk '{print $$3}' | xargs -r docker rmi -f
	@docker images | grep "challenge" | awk '{print $$3}' | xargs -r docker rmi -f
	@echo "$(YELLOW)🗑️  Removing volumes...$(NC)"
	@docker volume prune -f
	@echo "$(YELLOW)🗑️  Removing networks...$(NC)"
	@docker network prune -f
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

# ================================
# ADDITIONAL COMMANDS
# ================================

dev: ## 🛠️  Start development environment with hot-reload
	@echo "$(BLUE)🛠️  Starting development environment...$(NC)"
	@$(MAKE) -s check-docker
	@docker-compose -f $(DOCKER_COMPOSE_DEV_FILE) up --build
	@echo "$(GREEN)✅ Development environment started!$(NC)"

build: ## 🏗️  Build Docker images without starting services
	@echo "$(BLUE)🏗️  Building Docker images...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) build
	@echo "$(GREEN)✅ Images built successfully!$(NC)"

logs: ## 📜 Show service logs
	@echo "$(BLUE)📜 Showing service logs...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

status: ## 📊 Show status of all services
	@echo "$(BLUE)📊 Service status:$(NC)"
	@echo ""
	@docker-compose -f $(DOCKER_COMPOSE_FILE) ps

health: ## ❤️  Check API health
	@echo "$(BLUE)❤️  Checking API health...$(NC)"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "$(RED)❌ API not available$(NC)"

lint: ## 🔍 Run code linting
	@echo "$(BLUE)🔍 Running linting...$(NC)"
	@. $(VENV_NAME)/bin/activate && \
		flake8 src/ tests/ && \
		echo "$(GREEN)✅ Linting completed!$(NC)"

format: ## 🎨 Format code with black and isort
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	@. $(VENV_NAME)/bin/activate && \
		black src/ tests/ && \
		isort src/ tests/
	@echo "$(GREEN)✅ Code formatted!$(NC)"

type-check: ## 🔎 Check types with mypy
	@echo "$(BLUE)🔎 Checking types...$(NC)"
	@. $(VENV_NAME)/bin/activate && mypy src/
	@echo "$(GREEN)✅ Type checking completed!$(NC)"

coverage: ## 📊 Generate detailed coverage report
	@echo "$(BLUE)📊 Generating coverage report...$(NC)"
	@. $(VENV_NAME)/bin/activate && \
		python -m pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Report generated at htmlcov/index.html$(NC)"
	@open htmlcov/index.html 2>/dev/null || echo "$(BLUE)🌐 Open: htmlcov/index.html$(NC)"

docker-clean: ## 🧹 Clean only Docker resources related to project
	@echo "$(BLUE)🧹 Cleaning project Docker resources...$(NC)"
	@docker-compose -f $(DOCKER_COMPOSE_FILE) down --rmi all --volumes --remove-orphans
	@echo "$(GREEN)✅ Docker resources cleaned!$(NC)"

# ================================
# VERIFICATION FUNCTIONS
# ================================

check-requirements: ## 🔍 Verify that all necessary tools are installed
	@echo "$(YELLOW)🔍 Verifying necessary tools...$(NC)"
	@$(MAKE) -s check-python
	@$(MAKE) -s check-docker
	@echo "$(GREEN)✅ All tools are available!$(NC)"

check-python:
	@command -v python$(PYTHON_VERSION) >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1 || { \
		echo "$(RED)❌ Python $(PYTHON_VERSION)+ not found.$(NC)"; \
		echo "$(YELLOW)📦 To install Python:$(NC)"; \
		echo "  macOS: brew install python@$(PYTHON_VERSION)"; \
		echo "  Ubuntu/Debian: sudo apt-get install python$(PYTHON_VERSION) python$(PYTHON_VERSION)-venv"; \
		echo "  Windows: Download from https://python.org"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Python $(PYTHON_VERSION)+ found$(NC)"

check-docker:
	@command -v docker >/dev/null 2>&1 || { \
		echo "$(RED)❌ Docker not found.$(NC)"; \
		echo "$(YELLOW)📦 To install Docker:$(NC)"; \
		echo "  macOS: brew install --cask docker"; \
		echo "  Ubuntu: sudo apt-get install docker.io docker-compose"; \
		echo "  Windows: Download Docker Desktop from https://docker.com"; \
		exit 1; \
	}
	@command -v docker-compose >/dev/null 2>&1 || { \
		echo "$(RED)❌ Docker Compose not found.$(NC)"; \
		echo "$(YELLOW)📦 Docker Compose is required to run the project.$(NC)"; \
		exit 1; \
	}
	@docker info >/dev/null 2>&1 || { \
		echo "$(RED)❌ Docker daemon is not running.$(NC)"; \
		echo "$(YELLOW)🚀 Start Docker Desktop or run: sudo systemctl start docker$(NC)"; \
		exit 1; \
	}
	@echo "$(GREEN)✅ Docker and Docker Compose available$(NC)"

# ================================
# PROJECT INFORMATION
# ================================

info: ## 📋 Show project information
	@echo ""
	@echo "$(BLUE)🤖 Kopi Challenge - Persuasive Debate Chatbot API$(NC)"
	@echo "$(BLUE)======================================================$(NC)"
	@echo ""
	@echo "$(GREEN)📝 Description:$(NC)"
	@echo "  API for a chatbot that can maintain a debate and attempt"
	@echo "  to convince the opponent of its viewpoints, regardless"
	@echo "  of how irrational the position may be."
	@echo ""
	@echo "$(GREEN)🏗️  Architecture:$(NC)"
	@echo "  - Hexagonal Architecture (Ports & Adapters)"
	@echo "  - Domain-Driven Design (DDD)"
	@echo "  - FastAPI + Python 3.11"
	@echo "  - Docker containerization"
	@echo ""
	@echo "$(GREEN)🎭 Debate Personalities:$(NC)"
	@echo "  - Conspiracy Theorist"
	@echo "  - Skeptical Scientist" 
	@echo "  - Populist Debater"
	@echo ""

# Ensure 'help' is the default target if nothing is specified
.DEFAULT_GOAL := help
