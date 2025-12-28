from fastapi import APIRouter, HTTPException
from models import UserCreate, UserUpdate, User
from services.user_service import create_user, get_user_by_telegram_id, update_user_settings
from typing import Optional

router = APIRouter()

@router.post("/", response_model=User)
async def register_user(user: UserCreate):
    try:
        result = await create_user(user.telegram_id, user.full_name, user.email)
        if result:
            return result
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}", response_model=User)
async def get_user(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{telegram_id}", response_model=User)
async def update_user(telegram_id: int, user_update: UserUpdate):
    user = await update_user_settings(telegram_id, user_update.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
