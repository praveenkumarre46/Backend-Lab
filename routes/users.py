from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from utils import pwd_context
import schemas
import models
from database import get_db
from routes.oauth2 import get_current_user

router = APIRouter(prefix="", tags=["Users"])

@router.post("/usersignup", response_model=schemas.responecreate, status_code=status.HTTP_201_CREATED)
def newuser(
    usr: schemas.userschema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.users).filter(
        models.users.email == usr.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A User with this email is already registered",
        )

    hashed_password = pwd_context.hash(usr.password)
    new_user_login = models.users(
        email=usr.email,
        password=hashed_password,
    )
    db.add(new_user_login)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email is already registered",
        )
    db.refresh(new_user_login)
    return new_user_login


@router.post("/userlogin", response_model=schemas.responecreate)
def loginst(usr: schemas.userschema, db: Session = Depends(get_db)):
    st = db.query(models.users).filter(models.users.email == usr.email).first()
    if not st:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered",
        )
    if not pwd_context.verify(usr.password, st.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is incorrect",
        )
    return st


@router.get("/getuser/{id}", response_model=schemas.responecreate)
def getuser(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    user = db.query(models.users).filter(models.users.userid == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered",
        )
    if user.email != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user profile",
        )
    return user


@router.delete("/deleteuser/{user_id}")
async def deleteuser(user_id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(get_current_user)):
    usr=db.query(models.users).filter(models.users.userid==user_id).first()
    if not usr:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not available"))
    if usr.email != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own user account",
        )
    db.delete(usr)
    db.commit()
    return "Deleted User"