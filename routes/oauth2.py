from datetime import datetime, timedelta, timezone
from config import settings
import schemas
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


SECRET_KEY =settings.SECRET_KEY 
ALGORITHM = settings.ALGORITHM
EXPIRATION_TIME = settings.EXPIRATION_TIME


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)