
from pymongo import MongoClient
from datetime import timedelta

class MongoQueue:

    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, timeout=300):

        self.client = MongoClient()
        self.db = self.client.cache2
        self.timeout = timeout

    def push(self, url):
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass
