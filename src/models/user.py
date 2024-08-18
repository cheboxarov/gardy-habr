from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    BigInteger,
)
from db.core import Base
from sqlalchemy.orm import sessionmaker, relationship


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    full_name = Column(String)
    is_admin = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")
    promo = Column(String, default=None)
