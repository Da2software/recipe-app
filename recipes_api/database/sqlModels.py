from database.db_clients import PostgresDatabase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
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


class Comments(sqlBase):
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
    user = relationship(Users, backref='comments')


class StarsRecipe(sqlBase):
    __tablename__ = "stars_recipe"

    recipe_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    stars = Column(Integer, default=0)


sqlBase.metadata.create_all(bind=postgresManager.get_engine())
