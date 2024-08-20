from sqlalchemy import (
    Column,
    Integer,
    String,
    Float, ForeignKey,
)
from sqlalchemy.orm import relationship

from db.core import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    portfolio = Column(String)
    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", cascade="all, delete-orphan", back_populates="parent")

