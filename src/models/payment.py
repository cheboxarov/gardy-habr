from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from db.core import Base
from sqlalchemy.orm import sessionmaker, relationship


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    is_paid = Column(Boolean, default=False)
    order = relationship("Order", back_populates="payment")
