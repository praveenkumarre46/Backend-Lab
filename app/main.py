from fastapi import FastAPI

from app.api.routes import practice, users
from routes import users as student_users


app = FastAPI(title="Backend Lab API")

app.include_router(practice.router)
app.include_router(users.router)
app.include_router(student_users.router)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"message": "Backend Lab API is running"}