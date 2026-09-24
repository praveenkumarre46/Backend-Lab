from utils import pwd_context
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas,models
from routes.oauth2 import create_token,get_current_user
from database import get_db
router=APIRouter(tags=["Authentication"])

@router.get("/sigin",response_model=schemas.userresponse)
async def sigin(user:schemas.Createstudent,db:Session=Depends(get_db)):
    hased=pwd_context.hash(user.password)
    newuser=models.users(email=user.email, password=hased)
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser
    
@router.post("/login", response_model=schemas.token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usr = db.query(models.users).filter(
        models.users.email == user_credentials.username
    ).first()
    if not usr:
        usr = db.query(models.studentslog).filter(
            models.studentslog.email == user_credentials.username
        ).first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not pwd_context.verify(user_credentials.password, usr.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token({"sub": user_credentials.username})
    return {"access_token": token, "token_type": "bearer"}
