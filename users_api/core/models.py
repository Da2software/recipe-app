from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship

from .db_manager import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        self.hashed_password = bcrypt.hash(password)
