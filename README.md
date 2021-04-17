<p align="center">
<a href="https://bolsonaro-api.herokuapp.com/"><img alt="Bolsonaro API" src="https://github.com/MuriloScarpaSitonio/bolsonaro-api/blob/master/react/src/images/bozoQuote.png"></a>
</p>

<h1 align="center">Bolsonaro API</h1>

<p align="center">
<a href="https://twitter.com/ApiBolsonaro" target="_blank" rel="noopener noreferrer"><img alt="Bolsonaro API twitter" src="https://img.shields.io/twitter/follow/ApiBolsonaro?style=social"></a>
</p>

<p align="center">
<a href="https://travis-ci.com/github/MuriloScarpaSitonio/bolsonaro-api" target="_blank" rel="noopener noreferrer"><img alt="Build Status" src="https://travis-ci.com/MuriloScarpaSitonio/bolsonaro-api.svg?branch=master"></a>
<a href="https://coveralls.io/github/MuriloScarpaSitonio/bolsonaro-api?branch=master" target="_blank" rel="noopener noreferrer"><img alt="Coverage Status" src="https://coveralls.io/repos/github/MuriloScarpaSitonio/bolsonaro-api/badge.svg?branch=master"></a>
<a href="https://github.com/PyCQA/pylint" target="_blank" rel="noopener noreferrer"><img alt="Pylint Rating" src="https://mperlet.github.io/pybadge/badges/10.0.svg"></a>
<a href="https://github.com/psf/black" target="_blank" rel="noopener noreferrer"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="http://mypy-lang.org/" target="_blank" rel="noopener noreferrer"><img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/PyCQA/bandit" target="_blank" rel="noopener noreferrer"><img alt="Checked with bandit" src="https://img.shields.io/badge/bandit-checked-informational"></a>
<a href="https://django.doctor/" target="_blank" rel="noopener noreferrer"><img alt="Checked with bandit" src="https://img.shields.io/badge/django doctor-checked-informational"></a>
</p>

API pública de declarações e ações do presidente Bolsonaro e seu governo. Desenvolvida com **Django**, **React**, **PostgreSQL**, **Celery**, **Redis** e **Docker**.

## Instalação

Se você tem docker e docker-compose instalados, rode os seguintes comandos:
```
$ docker-compose build
$ docker-compose run django sh entrypoint.local.sh  # criação da estrutura do banco local e inserção dos dados
$ docker-compose up
```
Depois, visite http://127.0.0.1:3000/ para acessar o servidor de desenvolvimento do React e http://127.0.0.1:8000/api/v1/docs/ para ver a documentação e interagir com a API do django.

Na ausência de docker, você pode usar os comandos do Makefile:

```
make django
make react
```

## Contribuições
- Visite [/contribute](https://bolsonaro-api.herokuapp.com/contribute) e contribua com alguma das três ações citadas!
- React;
   - Testes, pipeline, code review e quaisquer ajuds no frontend são MUITO bem-vindas!
- Django:
   - Antes de enviar um PR, certifique-se de que o comando `make django-pipeline` não retorna nenhum erro.
- Entre em contato para enviar contribuições nos outros serviços de `docker-compose.production.yml`.


