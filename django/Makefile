.PHONY: clean create-venv setup-dev db-up code-convention test run pipeline backend

PIP := pip install -r
PROJECT_NAME := bolsonaro-api
PYTHON_VERSION := 3.8.2
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)
PYTEST_CONFIGS := --nomigrations --cov-report=term-missing  --cov-report=html --cov=. --disable-warnings

.pip:
	pip install pip --upgrade


setup-dev: .pip
	$(PIP) requirements/local.txt


setup-production: .pip
	$(PIP) requirements/production.txt


.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/


clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts


.create-venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)


create-venv: .create-venv setup-dev


db-up:
	python manage.py migrate


.db-populate-actions:
	python manage.py createactions


.db-populate-quotes:
	python manage.py createquotes


db-populate: db-up .db-populate-actions .db-populate-quotes


test:
	pytest $(PYTEST_CONFIGS)


code-convention:
	pylint_runner
	black . --check --exclude=migrations


security-checker:
	bandit -r . --exclude=/tests,/venv
# python manage.py check --deploy --fail-level=ERROR --settings=bolsonaro_api.settings.production


typing-checker:
	mypy . --exclude=venv --ignore-missing-imports


pipeline: test code-convention security-checker typing-checker


run:
	python manage.py runserver 0.0.0.0:8000


collectstatic:
	python manage.py collectstatic --noinput


all: setup-dev db-populate collectstatic run
