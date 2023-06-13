start:
	python3 manage.py runserver

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8
