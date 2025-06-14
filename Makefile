# Build configuration
# -------------------

APP_NAME := `sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
APP_VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
GIT_REVISION = `git rev-parse HEAD`

# Introspection targets
# ---------------------

.PHONY: help
help: header targets

.PHONY: header
header:
	@echo "\033[34mEnvironment\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@printf "\033[33m%-23s\033[0m" "APP_NAME"
	@printf "\033[35m%s\033[0m" $(APP_NAME)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "APP_VERSION"
	@printf "\033[35m%s\033[0m" $(APP_VERSION)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "GIT_REVISION"
	@printf "\033[35m%s\033[0m" $(GIT_REVISION)
	@echo "\n"

.PHONY: targets
targets:
	@echo "\033[34mDevelopment Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# Development targets
# -------------

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: run
run: start

.PHONY: start
start: ## Starts the server
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run python main.py

.PHONY: migrate
migrate: ## Run the migrations
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic upgrade head

.PHONY: rollback
rollback: ## Rollback migrations one level
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic downgrade -1

.PHONY: reset-database
reset-database: ## Rollback all migrations
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic downgrade base

.PHONY: generate-migration 
generate-migration: ## Generate a new migration
	$(eval include .env) 
	$(eval export $(sh sed 's/=.*//' .env)) 

	@read -p "Enter migration message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"

.PHONY: celery-worker
celery-worker: ## Start celery worker
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run celery -A worker worker -l info

.PHONY: create-default-user
create-default-user: ## Create default user (requires env vars: DEFAULT_USER_USERNAME, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD)
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	
	@if [ -z "$$DEFAULT_USER_USERNAME" ] || [ -z "$$DEFAULT_USER_EMAIL" ] || [ -z "$$DEFAULT_USER_PASSWORD" ]; then \
		echo "❌ Erro: Defina as variáveis de ambiente obrigatórias:"; \
		echo "   export DEFAULT_USER_USERNAME=seu_usuario"; \
		echo "   export DEFAULT_USER_EMAIL=seu_email@exemplo.com"; \
		echo "   export DEFAULT_USER_PASSWORD=sua_senha_segura"; \
		echo "   export DEFAULT_USER_IS_ADMIN=true  # (opcional)"; \
		echo ""; \
		echo "Ou adicione no arquivo .env:"; \
		echo "   DEFAULT_USER_USERNAME=seu_usuario"; \
		echo "   DEFAULT_USER_EMAIL=seu_email@exemplo.com"; \
		echo "   DEFAULT_USER_PASSWORD=sua_senha_segura"; \
		echo "   DEFAULT_USER_IS_ADMIN=true"; \
		exit 1; \
	fi
	
	PYTHONPATH=. poetry run python scripts/create_default_user.py

# Check, lint and format targets
# ------------------------------

.PHONY: check
check: check-format lint

.PHONY: check-format
check-format: ## Dry-run code formatter
	poetry run black ./ --check
	poetry run isort ./ --profile black --check

.PHONY: lint
lint: ## Run linter
	poetry run pylint ./api ./app ./core
 
.PHONY: format
format: ## Run code formatter
	poetry run black ./
	poetry run isort ./ --profile black

.PHONY: check-lockfile
check-lockfile: ## Compares lock file with pyproject.toml
	poetry lock --check

.PHONY: test
test: ## Run the test suite
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run pytest -vv -s --cache-clear ./