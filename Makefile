SERVER_PORT=5000

ifneq (,$(wildcard ./.dev.env))
	include .env
	export
endif

.PHONY : install setup tests check-types check check-full lint lint-changed serve pyclean migrate-local

install:
	poetry install

setup: install
	poetry run pre-commit install

test-with-coverage: migrate-local
	poetry run pytest --cov=app --cov-report term-missing:skip-covered --cov-report xml:.test-reports/coverage.xml --junitxml=.test-reports/test-run.xml


lint:
	poetry run pre-commit run --all-files

lint-changed:
	git status --porcelain | egrep -v '^(D |RM|R )' | cut -b 4- | xargs poetry run pre-commit run --files

lint-full-check: lint check-types

serve:
	poetry run flask run --host=0.0.0.0 --port=$(SERVER_PORT) --reload

pyclean:
	find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +

migrate-local:
	poetry run flask db upgrade
	

build:
	docker-compose build

up:
	docker-compose up -d

logs:
	docker-compose logs -f

down:
	docker-compose down -v
