from datetime import date
from fastapi import FastAPI
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from database import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)


class Visit(Base):
    __tablename__ = "visit"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.id"))
    arrival_date = Column(Date)
    departure_date = Column(Date)
    duration = Column(Integer)
    comment = Column(String)