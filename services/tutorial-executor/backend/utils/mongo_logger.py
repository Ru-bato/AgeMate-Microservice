from pymongo import MongoClient
import logging

class MongoDBLogHandler(logging.Handler):
    """Custom log handler to store logs in MongoDB."""
    def __init__(self, db_name, collection_name, mongo_uri="mongodb://localhost:27017/"):
        super().__init__()
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({"log": log_entry})

def setup_mongo_logger(db_name, collection_name):
    """Setup MongoDB logging."""
    logger = logging.getLogger("fastapi")
    mongo_handler = MongoDBLogHandler(db_name=db_name, collection_name=collection_name)
    logger.addHandler(mongo_handler)
    logger.setLevel(logging.INFO)
    return logger