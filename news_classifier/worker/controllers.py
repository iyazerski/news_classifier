from celery.signals import task_prerun

from news_classifier.common.processors import broker, db
from news_classifier.worker.tasks import classification


@task_prerun.connect
def on_task_init(*_, **__):
    """
    Establish DB connection on task init. Needed for a proper mongodb connection management
    during parallel celery tasks processing
    """

    db.connect()


@broker.app.task(name='classify_one', queue='classification')
def classify_one(**kwargs):
    classification.classify_one(**kwargs)


@broker.app.task(name='classify_many', queue='classification')
def classify_many(**kwargs):
    classification.classify_many(**kwargs)
