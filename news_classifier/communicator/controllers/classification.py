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

    # check queried data
    if not classification_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif classification_record.get('predictions') is None:
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY)
    elif classification_record['error']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=classification_record['error'])

    return classification_record['predictions']
