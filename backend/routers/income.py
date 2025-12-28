from fastapi import APIRouter, HTTPException
from models import IncomeCreate
from services.income_service import process_income, get_recent_income
from typing import List

router = APIRouter()

@router.post("/{telegram_id}")
async def add_income(telegram_id: int, income: IncomeCreate):
    try:
        result = await process_income(telegram_id, income.amount)
        if result:
            return result
        raise HTTPException(status_code=400, detail="Failed to process income")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}")
async def get_income_history(telegram_id: int, limit: int = 10):
    try:
        transactions = await get_recent_income(telegram_id, limit)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
