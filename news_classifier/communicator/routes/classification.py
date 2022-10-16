from fastapi import APIRouter

from news_classifier.communicator.scheme import classification as scheme
from news_classifier.communicator.controllers import classification as controllers

router = APIRouter()


@router.post(
    '',
    summary='Trigger predicting which news resource the provided texts belongs to and return current request ID',
    response_model=scheme.ClassifyResponse
)
def trigger_classification(request_body: scheme.ClassifyRequest):
    return controllers.trigger_classification(**request_body.dict())


@router.get(
    '/{request_id}',
    summary='Retrieve the result of the request sent to /classification',
    response_model=scheme.ClassificationResultResponse
)
def retrieve_classification_results(request_id: str):
    return controllers.retrieve_classification_results(request_id)
