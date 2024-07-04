import models

from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Person(BaseModel):
    first_name: str
    last_name: str


# Create a person
@app.post("/person")
async def create_person(person: Person, db: Session = Depends(get_db)):
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