import logging

from celery import Celery

from news_classifier.common.configs import BrokerConfigs

_logger = logging.getLogger(__name__)


class Broker:
    def __init__(self, configs: BrokerConfigs) -> None:
        self.configs = configs
        self.app = Celery(f'news_classifier_{self.configs.env}', broker=self.configs.dsn)
        self.app.conf.update(
            worker_hijack_root_logger=self.configs.hijack_root_logger,
        )

    def include_tasks(self):
        self.app.conf.update(
            include=['news_classifier.worker.controllers']
        )

    def produce(self, task_data: dict, task_name: str, queue: str, priority: int = None):
        task = self.app.send_task(task_name, kwargs=task_data, queue=queue, priority=priority)
        _logger.info(f'Task {task_name}[{task.id}] sent to {queue}')
