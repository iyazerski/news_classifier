from news_classifier.common.processors import configs as common_configs
from news_classifier.communicator.configs import Configs
from news_classifier.communicator.services import App

configs = Configs.from_package(__file__, common=common_configs)
app = App(configs=configs)
