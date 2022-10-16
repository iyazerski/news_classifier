import logging
from datetime import datetime

from bson import ObjectId

from news_classifier.common.processors import broker, db

_logger = logging.getLogger(__name__)


def classify(classification_id: str, text: str, max_predictions_num: int):
    """ Classify the text and save the prediction to db """

    classification_id = ObjectId(classification_id)
    classification_record = db.read(collection='classification', query={'_id': classification_id})
    if not classification_record:
        _logger.warning(f'Unable to classify the text: result {classification_id} is not found')
        return

    # TODO: call model for real predictions
    predictions = None

    db.create(
        collection='predictions',
        value={'classification_id': classification_id, 'text': text, 'predictions': predictions}
    )


def trigger(request_id: str, texts: list[str], **kwargs):
    """ Create a new db record and produce a batch of messages to `classify` task """

    result = db.create(
        collection='classification',
        value={'external_id': request_id, 'created_at': datetime.utcnow(), 'texts_num': len(texts)}
    )

    for text in texts:
        broker.produce(
            task_data={'classification_id': str(result['_id']), 'text': text, **kwargs},
            task_name='classify',
            queue='classification'
        )
