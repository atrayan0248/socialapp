.PHONY: run-server
run-server:
	poetry run python -m socialapp.manage runserver

.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python -m socialapp.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m socialapp.manage migrate

.PHONY: superuser
superuser:
	poetry run python -m socialapp.manage createsuperuser

.PHONY: update
update: install migrations migrate ;



