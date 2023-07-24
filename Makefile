PORT ?= 8000
start:
	python3 manage.py runserver

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8
	
MANAGE := poetry run python manage.py

migrate:
	 @$(MANAGE) migrate

migrations:
	@$(MANAGE) makemigrations

test:
	 poetry run python manage.py test

install:
	@poetry install

build: install migrate

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml
