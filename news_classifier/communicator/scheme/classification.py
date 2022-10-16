from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator


class ClassifyRequest(BaseModel):
    """ Schema for POST /classification request body """

    texts: list[str] = Field(..., min_items=1, description='List of news texts')
    max_predictions_num: Optional[int] = Field(None, description='Number of predictions', ge=1)

    @validator('texts', each_item=True)
    def texts_validator(cls, value):
        assert len(value) >= 100


class ClassifyResponse(BaseModel):
    """ Schema for POST /classification response body """

    request_id: str = Field(default_factory=str(uuid4()))


class ClassificationResultResponse(BaseModel):
    """ Schema for GET /classification response body """

    label: str
    proba: float
