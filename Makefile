.PHONY: help build dev prod up down logs clean shell migrate superuser sample-data backup restore

# Default target
help:
	@echo "FullMoon OJ - Docker Management Commands"
	@echo "========================================"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-build    - Build development container"
	@echo "  make dev-logs     - View development logs"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod         - Start production environment"
	@echo "  make prod-build   - Build production containers"
	@echo "  make prod-logs    - View production logs"
	@echo ""
	@echo "Database Commands:"
	@echo "  make migrate      - Run database migrations"
	@echo "  make superuser    - Create Django superuser"
	@echo "  make sample-data  - Load sample data"
	@echo "  make backup       - Backup database"
	@echo "  make restore      - Restore database"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make shell        - Open shell in web container"
	@echo "  make logs         - View all logs"
	@echo "  make clean        - Clean up containers and volumes"
	@echo "  make down         - Stop all containers"

# Development environment
dev: dev-build
	docker-compose -f docker-compose.dev.yml up -d

dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Production environment
prod: prod-build
	docker-compose --profile production up -d

prod-build:
	docker-compose --profile production build

prod-logs:
	docker-compose --profile production logs -f

# Common operations
up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Database operations
migrate:
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser

sample-data:
	docker-compose exec web python manage.py setup_sample_data

backup:
	docker-compose exec db pg_dump -U fullmoon_user fullmoon_oj > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@echo "Usage: make restore BACKUP_FILE=backup_filename.sql"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: Please specify BACKUP_FILE"; \
		echo "Example: make restore BACKUP_FILE=backup_20241201_120000.sql"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U fullmoon_user fullmoon_oj < $(BACKUP_FILE)

# Utility commands
shell:
	docker-compose exec web bash

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
	docker volume prune -f

# Health check
health:
	@echo "Checking container health..."
	@docker-compose ps
	@echo ""
	@echo "Checking application health..."
	@curl -f http://localhost:8000/ || echo "Application not responding"

# SSL certificate generation (for testing)
ssl:
	mkdir -p ssl
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout ssl/key.pem -out ssl/cert.pem \
		-subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Environment setup
env-setup:
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "Created .env file from env.example"; \
		echo "Please edit .env with your actual values"; \
	else \
		echo ".env file already exists"; \
	fi

# Quick start for new developers
quickstart: env-setup dev
	@echo "FullMoon OJ is starting up..."
	@echo "Wait a few moments, then visit: http://localhost:8000"
	@echo "Use 'make dev-logs' to view logs"
