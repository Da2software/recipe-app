from core.utils import EnvManager, SingletonMeta
from core.interfaces import IDatabase
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = EnvManager()


class MongoDatabase(IDatabase, metaclass=SingletonMeta):
    def __init__(self):
        self.client = MongoClient(ENV.get_env("MONGO_URL"))

    def close(self):
        pass

    def get_connection(self):
        return self.client


class PostgresDatabase(IDatabase, metaclass=SingletonMeta):
    def __init__(self):
        DATABASE_URL = f"postgresql+psycopg2://{ENV.get_env('SQL_USER')}:{ENV.get_env('SQL_PASS')}@{ENV.get_env('SQL_HOST')}/{ENV.get_env('SQL_DB')}"

        self._engine = create_engine(DATABASE_URL)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                          bind=self._engine)
        Base = declarative_base()
        self.client = Base

    def close(self):
        pass

    def get_connection(self):
        return self.client

    def get_session(self):
        return self._SessionLocal

    def get_engine(self):
        return self._engine
