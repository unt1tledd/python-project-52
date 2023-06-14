PORT ?= 8000
start:
	python3 manage.py runserver 0.0.0.0:$(PORT)

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations
