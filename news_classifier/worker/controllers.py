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


@broker.app.task(name='classify', queue='classification')
def classify_text(**kwargs):
    classification.classify(**kwargs)


@broker.app.task(name='trigger', queue='classification')
def trigger_classification(**kwargs):
    classification.trigger(**kwargs)
