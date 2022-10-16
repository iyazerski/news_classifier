from typing import Optional
from pathlib import Path

from pydantic import BaseModel

from news_classifier.common import configs

__all__ = ['ServerConfigs', 'Configs']


class ServerConfigs(BaseModel):
    host: str
    port: int
    enable_cors: bool

    @classmethod
    def from_context(cls, context: configs.Context) -> 'ServerConfigs':
        return cls(
            host=context.yml['server']['host'],
            port=context.env.get('PORT', default=context.yml['server']['port'], cast=int),
            enable_cors=context.env.get('ENABLE_CORS', default=context.yml['server']['enable_cors'], cast=bool)
        )


class PathConfigs(BaseModel):
    static: Optional[Path]
    templates: Optional[Path]

    @classmethod
    def from_context(cls, context: configs.Context) -> 'PathConfigs':
        return cls(
            static=Path(f'{context.package_dir}/static'),
            templates=Path(f'{context.package_dir}/templates')
        )


class Configs(configs.ConfigsABC):
    def __init__(self, *args, common: configs.Configs, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.common = common
        self.server = ServerConfigs.from_context(self.context)
        self.path = PathConfigs.from_context(self.context)
