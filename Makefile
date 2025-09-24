VENV := venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PY) manage.py

# DEFAULT VALUES (can be overridden by environment variables)
APP ?= clinic
DB_USER ?= vet_user
DB_NAME ?= vetclinic_db

.PHONY: venv install freeze run makemigrate migrate createsuperuser test lint format startapp up down ps wait_db shell

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools

install: venv
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

run:
	$(MANAGE) runserver

makemigrate:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

startapp:
	@if [ -d "$(APP)" ]; then \
		echo "App '$(APP)' já existe. Abortando."; \
		exit 1; \
	fi
	$(MANAGE) startapp $(APP)
	@echo "Lembre-se de adicionar '$(APP)' em INSTALLED_APPS no settings.py"

up:
	docker-compose up -d

down:
	docker-compose down

ps:
	docker-compose ps

test:
	$(VENV)/bin/pytest -q -vv -s

lint:
	$(VENV)/bin/flake8 .

format:
	$(VENV)/bin/black . && $(VENV)/bin/isort .