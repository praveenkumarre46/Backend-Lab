from fastapi import FastAPI
from routes import users, students,authentication,tweets
import models
from database import engine




models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(users.router)
app.include_router(students.router)
app.include_router(authentication.router)
app.include_router(tweets.router)



# @app.get('/')
# async def firstline():
#     return {"Message:":"Hi Good Morning!!"}

# @app.get("/name")
# async def name():
#     return {"Name:":"Praveen Kumar Reddy"}



# #Path Parameters

# @app.get("/fruits/{color}")
# async def fruits(color):
#     fruitss={
#         "Yellow":["Banana","Mango"],
#         "Red":["Apple","Tomato"],
#         "Green":["Avacado","guava"]
#     }
#     if color not in fruitss:
#         raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Color is not available"))
#     return fruitss[color]

# @app.get("/age/{age}")
# async def age(age:int):
#     return "Yes" if age>=18 else "No"

# #Predefined values
# class skills(str, Enum):
#     Fastap="FastAPI"
#     Sql="SQL"
#     Git="Git"

# @app.get("/skill/{skill_name}")
# async def skill(skill_name:skills):
#     if skill_name==skills.Fastap:
#         return "You are good at FastAPI"
#     elif skill_name==skills.Sql:
#         return "You are good at SQL"
#     else:
#         return "You are good at Git"

# class values(int,Enum):
#     one=1
#     two=2
#     three=3
#     four=4

# @app.get("/inte/{inte}")
# async def inte(inte:values):
#     return "You entered Correct value"


# #File path as Parameter
# @app.get("/File/{file_path:path}")
# async def filepath(file_path:str):
#     from pathlib import Path
#     file_path = Path(file_path)

#     if file_path.is_file():
#         return "File exists"
#     else:
#         return "File does not exist"



# #Query Parameter

# @app.get("/sum")
# async def query(v1:int | float, v2 : int | float, v3 : int =0, default : int = 0,Isaddition : bool=True ):
#     if Isaddition:
#         return v1+v2+v3+default
#     else:
#         return "Not Addition"

# #Multipath parameters
# @app.get("/Firstname/{first_name}/Middlename/{middle_name}/Lastname/{last_name}")
# async def fullname(first_name:str,middle_name:str,last_name:str):
#     return first_name+" "+middle_name+" "+last_name

# #Multiple path and query parameters

# @app.get("/User/{user_id}/Items/{item_name}")
# async def item(quantity: int=0,size :int =0,color:str | None = None):
#     colors=["Green","Orange","White","Black","Blue",None]
#     if quantity<0 or size<0 or color not in colors:
#         raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Quantity or Size or Color"))
#     return "Order Succesful"


# #HTTP Requests

# users=[]

# class user(BaseModel):
#     name:str
#     mobile:int
#     email:Optional[str] = None
#     Gender:str
#     Indian:bool=True


# class update(BaseModel):
#     name:Optional[str] = None
#     mobile:Optional[int] = None
#     email:Optional[str] = None
#     Gender:Optional[str] = None
#     Indian:Optional[bool] = None


# @app.get("/user/{user_name}/mobile/{mobile_no}")
# async def getuser(user_name:str,mobile_no:int):
#     for user in users:
#         if (user.name==user_name and user.mobile==mobile_no):
#             return user
#     raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Credentials"))


# @app.post("/newuser", status_code=status.HTTP_201_CREATED)
# async def newuser(new_user:user):
#     users.append(new_user)
#     return new_user

# @app.put("/update/{user_name}/mobile/{mobile_no}")
# async def update(user_name:str, mobile_no:int, details:update):
#     for index, existing_user in enumerate(users):
#         if existing_user.name == user_name and existing_user.mobile == mobile_no:
#             updated_user = existing_user.model_copy(update=details.model_dump(exclude_unset=True))
#             users[index] = updated_user
#             return updated_user
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
