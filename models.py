from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, Date, Float
from database import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)