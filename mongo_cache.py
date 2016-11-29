
import pickle
import zlib

from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient

class MongoCache:

    def __init__(self, expires=timedelta(days=30)):

        self.client = MongoClient()
        self.db = self.client.cache
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __setitem__(self, url, result):

        record = {'result': Binary(zlib.compress(pickle.dumps(result))),
                  'timestamp': datetime.utcnow()}

        self.db.webpage.update({'_id': url},
                               {'$set': record},
                               upsert=True)
        