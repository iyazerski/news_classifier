""" This module contains settings containers. Different settings are stored in different containers, main access is
provided with `Configs` class help.
"""

import logging.config
from pathlib import Path
from typing import Any, Union, Optional

from pydantic import BaseModel, Field, SecretStr
from ruamel.yaml import YAML

from news_classifier.common.configs.environment import Config as EnvironmentConfig

__all__ = [
    'Context',
    'ConfigsABC',
    'PathConfigs',
    'BrokerConfigs',
    'DatabaseConfigs',
    'Configs'
]


class Context(BaseModel):
    yml: Any
    env: Any
    package_dir: Path

    @classmethod
    def load(
        cls,
        package_dir: Union[str, Path],
        yml_path: Union[str, Path] = None,
        env_path: Union[str, Path] = None
    ) -> 'Context':
        """ Load configs from environment and YAML file """

        package_dir = Path(package_dir)
        if not package_dir.exists():
            raise FileNotFoundError(package_dir)

        env_path = Path(env_path or f'{package_dir.parent}/.env')
        env_config = EnvironmentConfig(env_path if env_path.exists() else '')

        yaml = YAML()
        yml_path = Path(yml_path or f'{package_dir}/configs/configs.yml')
        with yml_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        return cls(yml=yml_config, env=env_config, package_dir=package_dir)


class ConfigsABC:
    def __init__(self, package_dir: Union[str, Path], **kwargs) -> None:
        self.context = Context.load(package_dir, **kwargs)

    @classmethod
    def from_package(cls, entrypoint: str, **kwargs) -> 'ConfigsABC':
        package_dir = Path(entrypoint).parent
        return cls(
            package_dir=package_dir,
            yml_path=package_dir / 'configs/configs.yml',
            env_path=package_dir.parent.parent / '.env',
            **kwargs
        )


class PathConfigs(BaseModel):
    logs: Path
    models: Path
    static: Optional[Path]
    templates: Optional[Path]

    @classmethod
    def from_context(cls, context: Context) -> 'PathConfigs':
        obj = cls(
            logs=Path(context.yml['path']['logs']),
            models=Path(context.yml['path']['models']),
            static=Path(f'{context.package_dir}/static'),
            templates=Path(f'{context.package_dir}/templates')
        )
        obj.logs.mkdir(parents=True, exist_ok=True)
        return obj


class BrokerConfigs(BaseModel):
    env: str
    host: str
    port: int
    username: SecretStr
    password: SecretStr
    hijack_root_logger: bool

    @classmethod
    def from_context(cls, context: Context):
        return cls(
            env=context.env.get('ENV', default='dev'),
            username=context.env.get('BROKER_USERNAME', cast=str),
            password=context.env.get('BROKER_PASSWORD', cast=str),
            host=context.env.get('BROKER_HOST', default=context.yml['broker']['host'], cast=str),
            port=context.env.get('BROKER_PORT', default=context.yml['broker']['port'], cast=int),
            hijack_root_logger=context.yml['broker']['hijack_root_logger']
        )

    @property
    def dsn(self) -> str:
        return f'pyamqp://{self.username.get_secret_value()}:{self.password.get_secret_value()}' \
               f'@{self.host}:{self.port}/{self.env}'


class DatabaseConfigs(BaseModel):
    dialect: str
    username: SecretStr
    password: SecretStr
    host: str
    port: int
    name: str
    connect_retry_count: int
    connect_retry_delay: int
    other: dict = Field(default_factory=dict)

    @classmethod
    def from_context(cls, context: Context):
        return cls(
            dialect=context.env.get('DB_DIALECT', default=context.yml['db']['dialect'], cast=str),
            username=context.env.get('DB_USERNAME', cast=str),
            password=context.env.get('DB_PASSWORD', cast=str),
            host=context.env.get('DB_HOST', default=context.yml['db']['host'], cast=str),
            port=context.env.get('DB_PORT', default=context.yml['db']['port'], cast=int),
            name=context.yml['db']['name'],
            connect_retry_count=context.yml['db']['connect_retry']['count'],
            connect_retry_delay=context.yml['db']['connect_retry']['delay'],
            other=context.yml['db'].get('other', {})
        )

    @property
    def dsn(self) -> str:
        return f'{self.dialect}://{self.username.get_secret_value()}:{self.password.get_secret_value()}' \
               f'@{self.host}:{self.port}/'


class Configs(ConfigsABC):
    """ Container of all system configs """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.path = PathConfigs.from_context(self.context)
        self.configure_logging()

        self.broker = BrokerConfigs.from_context(self.context)
        self.db = DatabaseConfigs.from_context(self.context)

    def configure_logging(self) -> 'Configs':
        """ Add logs directory path to all file handlers and apply logging configs """

        if 'handlers' in self.context.yml['logging']:
            for key in self.context.yml['logging']['handlers']:
                handler_fname = self.context.yml['logging']['handlers'][key].get('filename')
                if handler_fname:
                    self.context.yml['logging']['handlers'][key]['filename'] = f'{self.path.logs}/{handler_fname}'
        logging.config.dictConfig(self.context.yml['logging'])
        return self
