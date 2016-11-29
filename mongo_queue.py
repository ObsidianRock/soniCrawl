
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

    def pop(self):

        item = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
            )

        if item:
            return item['_id']
        else:
            self.repair()
            raise KeyError()

    def repair(self):

        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        # $lt selects the documents where the value of the field is less than
        # the specified value.

        if record:
            print('Released:', record['_id'])


    def peek(self):
        item = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if item:
            return item['_id']


    def clear(self):
        self.db.crawl_queue.drop()