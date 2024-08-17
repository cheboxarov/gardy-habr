from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
)
from db.core import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Timer(Base):
    __tablename__ = "timers"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    discount_applied = Column(Boolean, default=False)
    order = relationship("Order")
