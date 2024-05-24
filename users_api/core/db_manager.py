from utils import EnvManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = EnvManager()

SQLALCHEMY_DATABASE_URL = ENV.get_env('SQL_DB')
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                            bind=engine)
_Base = declarative_base
