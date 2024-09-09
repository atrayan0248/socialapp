.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

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
update: install migrations migrate install-pre-commit;
