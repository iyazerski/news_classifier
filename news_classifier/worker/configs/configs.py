from pathlib import Path

from pydantic import BaseModel

from news_classifier.common import configs

__all__ = ['Configs', 'ClassificationConfigs']


class ClassificationConfigs(BaseModel):
    model_path: Path
    max_predictions_num: int

    @classmethod
    def from_context(cls, context: configs.Context) -> 'ClassificationConfigs':
        return cls(**context.yml['classification'])


class Configs(configs.ConfigsABC):
    def __init__(self, *args, common: configs.Configs, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.common = common
        self.classification = ClassificationConfigs.from_context(self.context)
