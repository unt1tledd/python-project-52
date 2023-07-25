PORT ?= 8000
start:
	python3 manage.py runserver

lint:
	poetry run flake8
	
MANAGE := poetry run python manage.py

install:
	@poetry install

migrate:
	 @$(MANAGE) migrate

migrations:
	@$(MANAGE) makemigrations

build: install migrate

test:
	 poetry run python manage.py test

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml
