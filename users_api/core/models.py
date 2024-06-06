from core.database import Base
import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy import Text


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_sub = Column(Boolean, default=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow,
                        nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        nullable=False)


class StarsRecipe(Base):
    __tablename__ = "starts_recipe"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(String, nullable=False)
    stars = Column(Integer, default=0)


class PassTokens(Base):
    __tablename__ = "pass_tokens"

    token = Column(String, index=True, primary_key=True)
    # minutes based, then 60*24 => one day
    expiration = Column(Integer, default=60 * 24)
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
