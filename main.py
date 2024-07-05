import models

from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class PersonBase(BaseModel):
    first_name: str
    last_name: str


class VisitBase(BaseModel):
    arrival_date: date
    departure_date: date
    duration: int
    comment: str


# Create a person
@app.post("/person")
async def create_person(person: PersonBase, db: Session = Depends(get_db)):
    person_obj = models.Person()
    person_obj.first_name = person.first_name
    person_obj.last_name = person.last_name
    db.add(person_obj)
    db.commit()

    return {"message": "Person added."}


# Get a single person
@app.get("/person/{person_id}")
async def get_person(person_id: int, db: Session = Depends(get_db)):

    person_model = db.query(models.Person).filter(
            models.Person.id == person_id).first()

    if person_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {person_id}: Does not exist"
        )

    return person_model


# Get all people
@app.get("/people")
async def get_people(db: Session = Depends(get_db)):
    return db.query(models.Person).all()


# Create a visit
@app.post("/visit/{person_id}")
async def create_visit(person_id: int, visit: VisitBase, db: Session = Depends(get_db)):
    visit_obj = models.Visit(person_id=person_id)
    visit_obj.arrival_date = visit.arrival_date
    visit_obj.departure_date = visit.departure_date
    visit_obj.duration = (visit.departure_date - visit.arrival_date).days
    visit_obj.comment = visit.comment
    db.add(visit_obj)
    db.commit()

    return {"message": "Visit added."}