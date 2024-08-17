from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from db.core import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    price = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("categories.id"), nullable=False)
