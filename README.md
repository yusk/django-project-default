# README

## env

* python 3.8.x
  * poetry
* redis

## setup

### mac

```bash
brew install mecab-ipadic
```

### ubuntu

```bash
sudo apt install mecab libmecab-dev mecab-ipadic-utf8
```

### all

```bash
cp .env.sample .env
poetry run poetry install
poetry run python manage.py migrate
```

## run

```bash
poetry run python manage.py runserver
```

## create user

```bash
poetry run python manage.py createsuperuser
```

## check api schema

```bash
# after run server
open localhost:8000/schema/ # need session login
```

## rollback

```bash
python manage.py showmigrations
 python manage.py migrate main 00xx  # rollback to 00xx
```

## httpie

```bash
http post http://localhost:8000/api/register/dummy/
http post http://localhost:8000/api/auth/user/ email=test@test.com password=testuser

http post http://localhost:8000/api/auth/refresh/ token=$TOKEN
http post http://localhost:8000/api/auth/verify/ token=$TOKEN

http http://localhost:8000/api/user/ Authorization:"JWT $TOKEN"
```

## wscat

### install

```bash
npm install -g wscat
```

### run

```bash
wscat -c localhost:8000/ws/room/test/ -H "Authorization:JWT $TOKEN"
```

## use doc2vec

need to set local/wikipedia/{jawiki.doc2vec.dbow300d.model|*.npy}

e.g. from https://yag-ays.github.io/project/pretrained_doc2vec_wikipedia/
