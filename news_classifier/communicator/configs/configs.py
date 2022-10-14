from pydantic import BaseModel

from news_classifier.common.configs import Context, Configs as CommonConfigs, ConfigsABC

__all__ = ['ServerConfigs', 'Configs']


class ServerConfigs(BaseModel):
    host: str
    port: int

    @classmethod
    def from_context(cls, context: Context) -> 'ServerConfigs':
        return cls(
            host=context.yml['server']['host'],
            port=context.env.get('PORT', default=context.yml['server']['port'], cast=int)
        )


class Configs(ConfigsABC):
    def __init__(self, *args, common: CommonConfigs, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.common = common
        self.server = ServerConfigs.from_context(self.context)
