from fastapi import APIRouter, HTTPException, status

from news_classifier.communicator.scheme.classification import ClassifyRequest, ClassifyResponse, ClassificationResultResponse
from news_classifier.common.processors import broker, db

router = APIRouter()


@router.post(
    '',
    summary='Trigger predicting which news resource the provided texts belongs to and return current request ID',
    response_model=ClassifyResponse
)
def classify_many(request_body: ClassifyRequest):
    response = ClassifyResponse()
    broker.produce(
        task_data={'request_id': response.request_id, **request_body.dict()},
        task_name='classify_many',
        queue='classification'
    )
    return response


@router.get(
    '/{request_id}',
    summary='Retrieve the result of the request sent to /classification',
    response_model=list[ClassificationResultResponse]
)
def classification_result(request_id: str):
    result = db.read(collection='results', query={'request_id': request_id})
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif not result['ready']:
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY)
    else:
        return result['predictions']
