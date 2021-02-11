#!/bin/bash
set -eu

poetry run python manage.py makemigrations
poetry run python manage.py migrate
