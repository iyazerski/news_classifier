from uuid import uuid4

from fastapi import HTTPException, status

from news_classifier.common.processors import db, broker


def trigger_classification(**kwargs) -> dict:
    """ Send request classification message to the queue """

    response = {'request_id': str(uuid4())}
    broker.produce(
        task_data={**response, **kwargs},
        task_name='trigger',
        queue='classification'
    )
    return response


def retrieve_classification_results(request_id: str) -> list[dict]:
    """ Check classification results and  """

    # query classification data from db
    classification_record = db.read(collection='classification', query={'external_id': request_id})
    if not classification_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # query predictions related to required classification
    result = db.read(collection='predictions', query={'classification_id': classification_record['_id']}, many=True)
    if len(result) < classification_record['texts_num']:
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY)

    return result
