from news_classifier.common.processors import broker, db

db.connect()
broker.include_tasks()
app = broker.app
