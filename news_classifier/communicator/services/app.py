import uvicorn
from fastapi import FastAPI
from starlette.routing import NoMatchFound

from news_classifier.communicator.configs import Configs


class App:
    def __init__(self, configs: Configs) -> None:
        self.server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        self.configs = configs.server

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

        self.server.include_router(index.router, tags=['index'])
        self.server.include_router(classification.router, prefix='/classification', tags=['classification'])

        return self
