#!/bin/bash
set -eu

pipenv run pipenv install
pipenv run python manage.py migrate --settings=config.settings.production
pipenv run python manage.py collectstatic --settings=config.settings.production
