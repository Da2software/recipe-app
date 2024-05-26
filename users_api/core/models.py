from core.database import Base
import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class PassTokens(Base):
    __tablename__ = "pass_tokens"

    token = Column(String, index=True, primary_key=True)
    # minutes based, then 60*24 => one day
    expiration = Column(Integer, default=60 * 24)
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
