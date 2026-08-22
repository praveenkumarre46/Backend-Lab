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
    
