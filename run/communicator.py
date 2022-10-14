from news_classifier.communicator.processors import app
from news_classifier.common.processors import db

db.connect()
app.include_routers()
server = app.server

if __name__ == '__main__':
    app.run()
