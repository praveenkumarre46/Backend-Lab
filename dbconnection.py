from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Student
app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class student(BaseModel):
    studentid: int = Field(alias="student_id")
    firstname:str
    lastname:str
    email:str
    phone:str
    dob:date
    eod:date

    model_config = {"from_attributes": True, "populate_by_name": True}

@app.get("/allstudents", response_model=list[student])
async def getstudents(db: Session = Depends(get_db)):
    return db.scalars(select(Student)).all()



@app.post("/newstudent", response_model=student, status_code=201)
async def newstudent(student: student, db: Session = Depends(get_db)):
    new_student = Student(
        student_id=student.studentid,
        firstname=student.firstname,
        lastname=student.lastname,
        email=student.email,
        phone=student.phone,
        dob=student.dob,
        enrollment_date=student.eod,
    )
    db.add(new_student)
    try:
        db.commit()
        db.refresh(new_student)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to insert student")
    return new_student

@app.put("/updatestudent/{id}", response_model=student)
async def updatestudent(id:int,student:student, db: Session = Depends(get_db)):
    existing_student = db.get(Student, id)
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    existing_student.firstname = student.firstname
    existing_student.lastname = student.lastname
    existing_student.email = student.email
    existing_student.phone = student.phone
    existing_student.dob = student.dob
    existing_student.enrollment_date = student.eod
    try:
        db.commit()
        db.refresh(existing_student)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update student")
    return existing_student

@app.delete("/deletestudent/{id}", response_model=student)
async def deletestudent(id:int, db: Session = Depends(get_db)):
    existing_student = db.get(Student, id)
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(existing_student)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete student")
    return existing_student

