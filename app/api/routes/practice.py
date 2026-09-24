from enum import Enum
from pathlib import Path

from fastapi import APIRouter, HTTPException, status


router = APIRouter(tags=["practice"])


@router.get("/fruits/{color}")
async def fruits(color: str) -> list[str]:
    fruit_by_color = {
        "Yellow": ["Banana", "Mango"],
        "Red": ["Apple", "Tomato"],
        "Green": ["Avocado", "Guava"],
    }
    if color not in fruit_by_color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color is not available",
        )
    return fruit_by_color[color]


@router.get("/age/{age}")
async def age(age: int) -> str:
    return "Yes" if age >= 18 else "No"


class Skill(str, Enum):
    FAST_API = "FastAPI"
    SQL = "SQL"
    GIT = "Git"


@router.get("/skill/{skill_name}")
async def skill(skill_name: Skill) -> str:
    messages = {
        Skill.FAST_API: "You are good at FastAPI",
        Skill.SQL: "You are good at SQL",
        Skill.GIT: "You are good at Git",
    }
    return messages[skill_name]


class AllowedValue(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


@router.get("/inte/{inte}")
async def integer_value(inte: AllowedValue) -> str:
    return "You entered Correct value"


@router.get("/file/{file_path:path}")
async def filepath(file_path: str) -> str:
    return "File exists" if Path(file_path).is_file() else "File does not exist"


@router.get("/sum")
async def query(
    v1: int | float,
    v2: int | float,
    v3: int = 0,
    default: int = 0,
    is_addition: bool = True,
) -> int | float | str:
    if not is_addition:
        return "Not Addition"
    return v1 + v2 + v3 + default


@router.get("/firstname/{first_name}/middlename/{middle_name}/lastname/{last_name}")
async def fullname(first_name: str, middle_name: str, last_name: str) -> str:
    return f"{first_name} {middle_name} {last_name}"


@router.get("/user/{user_id}/items/{item_name}")
async def item(
    user_id: str,
    item_name: str,
    quantity: int = 0,
    size: int = 0,
    color: str | None = None,
) -> str:
    valid_colors = {"Green", "Orange", "White", "Black", "Blue", None}
    if quantity < 0 or size < 0 or color not in valid_colors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Quantity or Size or Color",
        )
    return "Order Successful"