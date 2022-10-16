import uvicorn
from fastapi import FastAPI, Request, status
from starlette.routing import NoMatchFound
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from news_classifier.communicator.configs import Configs


class App:
    def __init__(self, configs: Configs) -> None:
        self.server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        self.configs = configs.server

        if self.configs.enable_cors:
            self.enable_cors()

        # mount templates
        if configs.path.templates.exists():
            self.templates = Jinja2Templates(configs.path.templates.as_posix())

        # mount static
        if configs.path.static.exists():
            self.server.mount('/static', StaticFiles(directory=configs.path.static.as_posix()), name='static')

    def enable_cors(self) -> 'App':
        """ Enable CORS for all origins, methods and headers. Do not enable CORS on production servers

        Notes
        -----

        Read more about CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
        """

        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        return self

    def url_for(self, endpoint: str, **kwargs) -> str:
        """ Generate relative URL for `endpoint` """

        endpoint_parts = endpoint.split('.')
        endpoint_tags = endpoint_parts[:-1]
        endpoint_name = endpoint_parts[-1]
        if not endpoint_tags or not endpoint_name:
            raise NoMatchFound(endpoint, kwargs)
        for route in self.server.routes:
            if endpoint_name != route.name or any(tag not in getattr(route, 'tags', []) for tag in endpoint_tags):
                continue
            try:
                return route.url_path_for(endpoint_name, **kwargs)
            except NoMatchFound:
                pass
        raise NoMatchFound(endpoint, kwargs)

    def render_template(self, template: str, request: Request, status_code: int = status.HTTP_200_OK, **kwargs):
        """ Render specified `template` with data from `kwargs` """

        kwargs.update(request=request, urlfor=self.url_for)
        return self.templates.TemplateResponse(name=template, context=kwargs, status_code=status_code)

    def run(self):
        """ Start `uvicorn` server from code """

        uvicorn.run(
            self.server,
            host=self.configs.host,
            port=self.configs.port,
            proxy_headers=True,
            forwarded_allow_ips='*'
        )

    def include_routers(self) -> 'App':
        """ Main application method: connect all exceptions handlers, endpoints and blueprints to app """

        from news_classifier.communicator.routes import index, classification
        from news_classifier.communicator.services import exceptions  # noqa

        self.server.include_router(index.router, tags=['index'])
        self.server.include_router(classification.router, prefix='/classification', tags=['classification'])

        return self
