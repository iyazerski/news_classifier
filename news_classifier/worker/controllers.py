import logging

from celery.signals import task_prerun

from news_classifier.common.processors import broker, db
from news_classifier.worker.tasks import classification

_logger = logging.getLogger(__name__)


@task_prerun.connect
def on_task_init(*_, **__):
    db.connect()


@broker.app.task(name='classify_one', queue='classification')
def classify_one(*args, **kwargs):
    classification.classify_one(*args, **kwargs)


@broker.app.task(name='classify_many', queue='classification')
def classify_many(*args, **kwargs):
    classification.classify_many(*args, **kwargs)
