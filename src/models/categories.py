from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)
from db.core import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    portfolio = Column(String)
