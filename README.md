# Django Project Default

## env

* python 3.6.x
  * pipenv

## setup

```bash
pipenv run pipenv install
pipenv run python manage.py migrate
```

## run

```bash
pipenv run python manage.py runserver
```

## httpie

```bash
http post http://localhost:8000/api/auth/user/ email=test@test.com password=testuser
http post http://localhost:8000/api/auth/dummy/ 

http post http://localhost:8000/api/auth/refresh/ token={token}
http post http://localhost:8000/api/auth/verify/ token={token}

http http://localhost:8000/api/user/ Authorization:"JWT {token}"
```


