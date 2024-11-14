from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Book(Base):
    __tablename__ = "library"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    pages = Column(Integer)
    author = Column(String, unique=True, index=True)
