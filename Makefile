PORT ?= 8000
start:
	python3 manage.py runserver

lint:
	poetry run flake8
	
MANAGE := poetry run python manage.py

migrate:
	 @$(MANAGE) migrate

migrations:
	@$(MANAGE) makemigrations

test:
	 poetry run python manage.py test

install: .env
	@poetry install

build: install migrate

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml
