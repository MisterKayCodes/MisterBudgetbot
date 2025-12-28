from fastapi import APIRouter, HTTPException
from services.accounts_service import get_all_accounts, get_total_balance
from typing import List

router = APIRouter()

@router.get("/{telegram_id}")
async def list_accounts(telegram_id: int):
    try:
        accounts = await get_all_accounts(telegram_id)
        return accounts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/balance")
async def get_balance(telegram_id: int):
    try:
        balance = await get_total_balance(telegram_id)
        return {"total_balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
