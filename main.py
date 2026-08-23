from enum import Enum
from fastapi import FastAPI 

app=FastAPI()

@app.get('/')
async def firstline():
    return {"Message:":"Hi Good Morning!!"}

@app.get("/name")
async def name():
    return {"Name:":"Praveen Kumar Reddy"}



#Path Parameters

@app.get("/fruits/{color}")
async def fruits(color):
    fruitss={
        "Yellow":["Banana","Mango"],
        "Red":["Apple","Tomato"],
        "Green":["Avacado","guava"]
    }
    return fruitss[color] if color in fruitss else "Not available"

@app.get("/age/{age}")
async def age(age:int):
    return "Yes" if age>=18 else "No"

#Predefined values
class skills(str, Enum):
    Fastap="FastAPI"
    Sql="SQL"
    Git="Git"

@app.get("/skill/{skill_name}")
async def skill(skill_name:skills):
    if skill_name==skills.Fastap:
        return "You are good at FastAPI"
    elif skill_name==skills.Sql:
        return "You are good at SQL"
    else:
        return "You are good at Git"

class values(int,Enum):
    one=1
    two=2
    three=3
    four=4

@app.get("/inte/{inte}")
async def inte(inte:values):
    return "You entered Correct value"


#File path as Parameter
@app.get("/File/{file_path:path}")
async def filepath(file_path:str):
    from pathlib import Path
    file_path = Path(file_path)

    if file_path.is_file():
        return "File exists"
    else:
        return "File does not exist"



#Query Parameter

@app.get("/sum")
async def query(v1:int | float, v2 : int | float, v3 : int =0, default : int = 0,Isaddition : bool=True ):
    if Isaddition:
        return v1+v2+v3+default
    else:
        return "Not Addition"

#Multipath parameters
@app.get("/Firstname/{first_name}/Middlename/{middle_name}/Lastname/{last_name}")
async def fullname(first_name:str,middle_name:str,last_name:str):
    return first_name+" "+middle_name+" "+last_name

#Multiple path and query parameters

@app.get("/User/{user_id}/Items/{item_name}")
async def item(quantity: int=0,size :int =0,color:str | None = None):
    colors=["Green","Orange","White","Black","Blue"]
    if quantity<0 or size<0 or color not in colors:
        return "Invalid Quantity or Size or color"
    return "Order Succesful"