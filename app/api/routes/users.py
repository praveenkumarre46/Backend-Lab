from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/users", tags=["users"])
users: list[User] = []


class User(BaseModel):
    name: str
    mobile: int
    email: str | None = None
    gender: str
    indian: bool = True


class UserUpdate(BaseModel):
    name: str | None = None
    mobile: int | None = None
    email: str | None = None
    gender: str | None = None
    indian: bool | None = None


@router.get("/{user_name}/mobile/{mobile_no}", response_model=User)
async def get_user(user_name: str, mobile_no: int) -> User:
    for user in users:
        if user.name == user_name and user.mobile == mobile_no:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: User) -> User:
    users.append(new_user)
    return new_user


@router.patch("/{user_name}/mobile/{mobile_no}", response_model=User)
async def update_user(
    user_name: str,
    mobile_no: int,
    details: UserUpdate,
) -> User:
    for index, user in enumerate(users):
        if user.name == user_name and user.mobile == mobile_no:
            updated_user = user.copy(update=details.dict(exclude_unset=True))
            users[index] = updated_user
            return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )