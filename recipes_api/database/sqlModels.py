from database.db_clients import PostgresDatabase
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import datetime

postgresManager = PostgresDatabase()
sqlBase = postgresManager.get_connection()


class Users(sqlBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


sqlBase.metadata.create_all(bind=postgresManager.get_engine())
