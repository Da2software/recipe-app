from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.utils import EnvManager

env = EnvManager()

SQLALCHEMY_DATABASE_URL = connection_string = f'postgresql+psycopg2://{env.get_env("SQL_USER")}:{env.get_env("SQL_PASS")}@{env.get_env("SQL_HOST")}/{env.get_env("SQL_DB")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
