#!/bin/bash
set -eu

poetry install
poetry run python manage.py migrate --settings=config.settings.production
poetry run python manage.py seed --settings=config.settings.production
poetry run python manage.py compilescss --settings=config.settings.production
poetry run python manage.py collectstatic --ignore=*.scss --settings=config.settings.production
poetry run python manage.py compilescss --delete-files --settings=config.settings.production
poetry run python manage.py compress --settings=config.settings.production
