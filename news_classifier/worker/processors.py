from news_classifier.worker.configs import Configs
from news_classifier.common.processors import configs as common_configs
from news_classifier.worker.services import NewsClassifier

configs = Configs.from_package(__file__, common=common_configs)
news_classifier = NewsClassifier(configs=configs.classification)
