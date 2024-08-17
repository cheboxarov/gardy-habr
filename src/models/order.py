from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    DateTime,
    ForeignKey,
)
from db.core import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    category_id = Column(
        BigInteger, ForeignKey("categories.id")
    )  # Внешний ключ на таблицу categories
    description = Column(String)
    deadline = Column(String)
    deadline_hours = Column(Integer)
    price = Column(String)
    status = Column(String)  # Pending, Accepted, Rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    category = relationship("Category")  # Убедитесь, что Category определена правильно
    payment = relationship("Payment", back_populates="order", uselist=False)
