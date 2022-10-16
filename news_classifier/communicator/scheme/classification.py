import json
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator

from news_classifier.communicator.processors import configs

with open(configs.context.package_dir / 'scheme/examples.json', 'r', encoding='utf-8') as fp:
    _examples = json.load(fp)


class ClassifyRequest(BaseModel):
    """ Schema for POST /classification request body """

    texts: list[str] = Field(
        ..., min_items=1, description='List of news texts', example=_examples['ClassifyRequest']['texts']
    )
    max_predictions_num: Optional[int] = Field(None, description='Number of predictions', ge=1)

    @validator('texts', each_item=True)
    def texts_validator(cls, value):
        assert len(value) >= 100
        return value


class ClassifyResponse(BaseModel):
    """ Schema for POST /classification response body """

    request_id: str = Field(default_factory=str(uuid4()))


class ClassificationResultResponseItem(BaseModel):
    """ Schema for GET /classification response body """

    class Prediction(BaseModel):
        label: str
        proba: float

    text: str
    predictions: list[Prediction]


ClassificationResultResponse = list[ClassificationResultResponseItem]
