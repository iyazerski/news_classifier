import logging
from datetime import datetime

from news_classifier.common.processors import db
from news_classifier.worker.processors import news_classifier

_logger = logging.getLogger(__name__)


def classify_texts(request_id: str, texts: list[str], **kwargs):
    """ Classify provided texts and save results to db """

    result = db.create(
        collection='classification',
        value={'external_id': request_id, 'created_at': datetime.utcnow(), 'ready': False}
    )

    error = None
    predictions = None
    try:
        predictions = news_classifier.predict(texts, **kwargs)
    except Exception as e:
        error = str(e)
        _logger.exception(e)

    db.update(
        collection='classification',
        query={'_id': result['_id']},
        value={'$set': {'predictions': predictions, 'error': error}}
    )
