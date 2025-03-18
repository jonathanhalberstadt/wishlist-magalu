COMPOSE=docker-compose

build:
	$(COMPOSE) build

start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

exec:
	$(COMPOSE) exec app bash

migrate:
	$(COMPOSE) exec app bash -c "python -m flask db init"
	$(COMPOSE) exec app bash -c "python -m flask db migrate -m 'Criando tabelas'"
	$(COMPOSE) exec app bash -c "python -m flask db upgrade"

lint:
	(command -v pylint || pip install pylint) && find . -type f -name "*.py" | xargs pylint

test:
	$(COMPOSE) exec app bash -c "python -m unittest discover tests"

bandit:
	$(COMPOSE) exec app bash -c "python -m bandit -r . -ll"

logs:
	docker logs -f wishlist-magalu

## Version management
release:
ifeq ($(branch),master)
	npm run release
	git push origin master
	git push --tags
else
	@echo "You need to be in branch master"
endif

## Prerelease
prerelease:
	npm run release -- --prerelease
	git push origin $(git symbolic-ref --short HEAD)
	git push --tags
