# Define default target
.DEFAULT_GOAL := help
.PHONEY: help build generate-kong-config up down generate-jwt test

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Builds upstream app
	docker-compose build upstream-app

generate-kong-config: ## Generate the kong.yml file
	@cd kong && ./generate_kong_config.sh && cd ..

up: generate-kong-config build ## Start the Docker Compose
	docker-compose up

down: ## Stop the Docker Compose
	docker-compose down

generate-jwt: ## Generate a JWT token
	@cd jwt && python3 generate_jwt.py --expiry 1 app-user && cd ..

test: ## Test the API with an API Token
	@./test.sh