from pydantic import BaseModel,EmailStr
from datetime import datetime,date

class Student(BaseModel):
    student_id: int
    firstname: str
    lastname: str
    email: str
    phone: str
    dob: date
    enrollment_date: date


class result(BaseModel):
    student_id: int
    firstname: str
    lastname: str

    model_config = {"from_attributes": True}


class Createstudent(BaseModel):
    email:EmailStr
    password:str

class responecreate(BaseModel):
    userid:int
    email:str
    createat:datetime
    model_config={"from_attributes":True}

class userresponse(BaseModel):
    email:str
    createat:datetime
    model_config={"from_attributes":True}

class token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: str
    

class userschema(BaseModel):
    email:EmailStr
    password:str
    

class TwitterCreate(BaseModel):
    content: str

class TwitterUser(BaseModel):
    userid: int
    email: str
    createat: datetime

    model_config = {"from_attributes": True}


class twitternewuser(BaseModel):
    tweetid: int
    userid: int
    content: str
    createdat: datetime
    user: TwitterUser

    model_config = {"from_attributes": True}