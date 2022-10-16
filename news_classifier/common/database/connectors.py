import logging
import time
from typing import Optional

from pymongo import MongoClient

from news_classifier.common.configs import DatabaseConfigs

_logger = logging.getLogger(__name__)


class Database:
    def __init__(self, configs: DatabaseConfigs):
        self.configs = configs
        self.engine: Optional[MongoClient] = None

    def connect(self, retry_count: int = None) -> 'Database':
        """ Connect to db. Will try to connect `retry_count` times if connection errors occur  """

        if retry_count is None:
            retry_count = self.configs.connect_retry_count

        try:
            self.engine = MongoClient(self.configs.dsn, **self.configs.other)
        except Exception as e:
            if retry_count:
                _logger.warning(
                    f'Failed to connect to DB at {self.configs.host}:{self.configs.port}. '
                    f'Trying to reconnect after {self.configs.connect_retry_delay}s ({retry_count} attempts left)'
                )
                time.sleep(self.configs.connect_retry_delay)
                self.connect(retry_count=retry_count - 1)
            else:
                raise e

        # create indexes
        self.get_collection('classification').create_index('external_id')

        return self

    def get_collection(self, collection: str):
        return self.engine[self.configs.name][collection]

    def create(self, collection: str, value: dict) -> dict:
        value['_id'] = self.get_collection(collection).insert_one(value).inserted_id
        return value

    def read(self, collection: str, query: dict, many: bool = False) -> dict:
        col = self.get_collection(collection)
        return list(col.find(query)) if many else col.find_one(query)

    def update(self, collection: str, query: dict, value: dict):
        self.get_collection(collection).update_one(query, value)

    def delete(self, collection: str, query: dict, many: bool = False) -> int:
        col = self.get_collection(collection)
        return (col.delete_many if many else col.delete_one)(query).deleted_count
