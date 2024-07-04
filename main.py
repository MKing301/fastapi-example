import models

from datetime import date
from fastapi import FastAPI, Depends
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
async def create_item(person: Person, db: Session = Depends(get_db)):
    person_obj = models.Person()
    person_obj.first_name = person.first_name
    person_obj.last_name = person.last_name
    db.add(person_obj)
    db.commit()

    return {"message": "Person added."}


# Get all people
@app.get("/people")
async def get_people(db: Session = Depends(get_db)):
    return db.query(models.Person).all()