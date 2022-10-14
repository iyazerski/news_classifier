from news_classifier.common.database import Database
from news_classifier.common.messaging import Broker
from news_classifier.common.configs import Configs


configs = Configs.from_package(entrypoint=__file__)
broker = Broker(configs=configs.broker)
db = Database(configs=configs.db)
