from fastapi import APIRouter, HTTPException, Depends
from models import TrialCodeGenerate
from services.admin_service import (
    toggle_subscription_mode,
    generate_trial_code,
    get_subscribers_list,
    get_bot_statistics,
    get_all_users,
    delete_all_users
)
from config import settings

router = APIRouter()

def verify_admin(telegram_id: int):
    if telegram_id not in settings.admin_ids_list:
        raise HTTPException(status_code=403, detail="Admin access required")
    return telegram_id

@router.post("/subscription-mode/{telegram_id}")
async def toggle_sub_mode(telegram_id: int):
    verify_admin(telegram_id)
    try:
        result = await toggle_subscription_mode()
        return {"subscription_mode": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/trial-code/{telegram_id}")
async def create_trial_code(telegram_id: int, code_gen: TrialCodeGenerate):
    verify_admin(telegram_id)
    try:
        code = await generate_trial_code(code_gen.duration_days)
        return {"code": code, "duration_days": code_gen.duration_days}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscribers/{telegram_id}")
async def list_subscribers(telegram_id: int):
    verify_admin(telegram_id)
    try:
        subscribers = await get_subscribers_list()
        return {"subscribers": subscribers}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/statistics/{telegram_id}")
async def bot_stats(telegram_id: int):
    verify_admin(telegram_id)
    try:
        stats = await get_bot_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{telegram_id}")
async def list_all_users(telegram_id: int):
    verify_admin(telegram_id)
    try:
        users = await get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{telegram_id}")
async def delete_users(telegram_id: int):
    verify_admin(telegram_id)
    try:
        result = await delete_all_users()
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
