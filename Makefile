# Takes the first target as command
Command := $(firstword $(MAKECMDGOALS))
# Skips the first word
Arguments := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

build:
	docker-compose -f docker/docker-compose.yml --env-file .env up --build

build-d:
	docker-compose -f docker/docker-compose.yml --env-file .env up --build -d

down:
	docker-compose -f docker/docker-compose.yml --env-file .env down

down-v:
	docker-compose -f docker/docker-compose.yml --env-file .env down -v

# Example: make bash web
bash:
	docker exec -it $(Arguments) bash

# Example: make log db
log:
	docker logs -f $(Arguments) 2>&1 | ccze -m ansi 

# Example: make migra "create_group_table"
migra:
	alembic revision --autogenerate -m $(Arguments)

upg:
	alembic upgrade head

# Example: make exec cache redis-cli
exec:
	docker exec -it $(Arguments)

lint:
	PYTHONPATH=. python app/scripts/tools/lint.py

format:
	PYTHONPATH=. python app/scripts/tools/format.py

reg:
	PYTHONPATH=. python app/scripts/tools/docker_registry.py
