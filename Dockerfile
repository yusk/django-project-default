FROM python:3.8-slim as builder

WORKDIR /tmp

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -f requirements.txt > requirements.txt


FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/html/

COPY --from=builder /tmp/requirements.txt .

RUN apt update

# for mysqlclient
RUN apt install -y default-libmysqlclient-dev

# for uwsgi
RUN apt install -y gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
