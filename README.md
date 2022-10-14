# news_classifier

## Requirements

- [python](https://www.python.org/downloads/)

- [docker](https://docs.docker.com/get-docker/)

- [docker-compose](https://docs.docker.com/compose/install/)

- [pydeployhelp](https://pypi.org/project/pydeployhelp/)

## Quickstart

Create `.env` file in project root with following content (replace example values to real):

```text
# common
PROJECT_SLUG=news_classifier
ENV=dev
COMMUNICATOR_REPLICAS_NUM=1
WORKER_REPLICAS_NUM=1
VOLUMES_ROOT=/home/user/news_classifier

# communicator
PORT=8080
DNS=some_dns.com

# db
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=user
DB_PASSWORD=password

# broker
BROKER_HOST=localhost
BROKER_PORT=5672
BROKER_USERNAME=user
BROKER_PASSWORD=password
```

Run\build\stop all\any services:

```console
user@host:~/news_classifier$ pydeployhelp
```

## Development

To run project in development mode you need to install requirements:

```console
user@host:~/news_classifier$ python -m venv venv && source venv/bin/activate
(venv) user@host:~/news_classifier$ pip install -r requirements/dev.txt
```

And then install package in dev mode:

```console
(venv) user@host:~/news_classifier$ python setup.py develop
```
