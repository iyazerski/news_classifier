from fastapi import APIRouter, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse

from news_classifier import __version__
from news_classifier.communicator.processors import app

router = APIRouter()


@router.get('/', include_in_schema=False)
def index(_: Request) -> RedirectResponse:
    return RedirectResponse(app.url_for('index.healthcheck'))


@router.get('/openapi.json', include_in_schema=False)
def openapi():
    return JSONResponse(get_openapi(title='News classifier', version=__version__, routes=app.server.routes))


@router.get('/docs', include_in_schema=False)
def documentation():
    return get_swagger_ui_html(openapi_url=app.url_for('index.openapi'), title='docs')


@router.get('/healthcheck')
def healthcheck():
    return PlainTextResponse(content='It works', status_code=status.HTTP_200_OK)
