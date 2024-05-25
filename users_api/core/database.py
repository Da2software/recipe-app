from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.utils import EnvManager

env = EnvManager()

SQLALCHEMY_DATABASE_URL = env.get_env("SQL_DB")

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
