from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def create_tables():
    from models import User, Timer, Payment, Category, Order, Price

    Base.metadata.create_all(engine)
