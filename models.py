from sqlalchemy import Column, Date, DateTime, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Student(Base):
    __tablename__="StudentsMCA"
    student_id = Column(Integer, primary_key=True)
    firstname=Column(String,nullable=False)
    lastname=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    phone=Column(String,nullable=False)
    dob=Column(Date,nullable=False)
    enrollment_date=Column(Date,nullable=False)
    
class studentsbase(Base):
    __tablename__ = "studentbase"
    userid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    createat = Column(DateTime, default=datetime.utcnow)


class studentslog(Base):
    __tablename__ = "studentlog"
    userid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    createat = Column(DateTime, default=datetime.utcnow)

class users(Base):
    __tablename__="users"
    userid=Column(Integer,primary_key=True,autoincrement=True)
    email=Column(String,nullable=True)
    password=Column(String,nullable=False)
    createat = Column(DateTime, default=datetime.utcnow)

class Twitter(Base):
    __tablename__="Tweets"
    tweetid=Column(Integer,autoincrement=True,primary_key=True)
    userid=Column(Integer,ForeignKey("users.userid", ondelete="CASCADE"),nullable=False)
    content=Column(String,nullable=False)
    createdat=Column(DateTime,default=datetime.utcnow)

    user=relationship("users")

class Likes(Base):
    __tablename__="Likes"
    tweetid=Column(Integer,ForeignKey("Tweets.tweetid",ondelete="CASCADE"),nullable=False,primary_key=True)
    userid=Column(Integer,ForeignKey("users.userid", ondelete="CASCADE"),nullable=False,primary_key=True)
