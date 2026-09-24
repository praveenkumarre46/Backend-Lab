from fastapi import Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session

import schemas
import models
from database import get_db


router = APIRouter(prefix="", tags=["Students"])

@router.get("/mcastudents",response_model=schemas.result)
async def mcastudents(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@router.get("/student/{id}",response_model=schemas.result)
async def studentwith(id:int,db:Session=Depends(get_db)):
    stud=db.query(models.Student).filter(models.Student.student_id==id).first()
    if not stud:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not Found"))
    return stud

@router.post("/newstudent",response_model=schemas.result)
async def newstudents(student:schemas.Student,db:Session=Depends(get_db)):
    newst=models.Student(**student.dict())
    db.add(newst)
    db.commit()
    db.refresh(newst)
    return newst


@router.delete("/deletestudent/{id}",response_model=schemas.result)
async def delstudent(id: int, db: Session = Depends(get_db)):
    stud = (
        db.query(models.Student)
        .filter(models.Student.student_id == id)
        .first()
    )

    if not stud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    db.delete(stud)
    db.commit()

    return {"message": "Student deleted successfully"}

@router.put("/updatestudent/{id}",response_model=schemas.result)
async def updstudent(id:int,student:schemas.Student,db:Session=Depends(get_db)):
    st_query=db.query(models.Student).filter(models.Student.student_id==id)
    st=st_query.first()
    if not st:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student doesn't exist"))
    st_query.update(student.dict(),synchronize_session=False)
    db.commit()
    return st_query.first()
