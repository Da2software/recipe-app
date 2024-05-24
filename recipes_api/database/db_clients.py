from core.utils import EnvManager, SingletonMeta
from core.interfaces import IDatabase
from pymongo import MongoClient

ENV = EnvManager()


class MongoDatabase(IDatabase, metaclass=SingletonMeta):
    def __init__(self):
        self.client = MongoClient(ENV.get_env("MONGO_URL"))

    def close(self):
        pass

    def get_connection(self):
        return self.client
