from fastapi import APIRouter, HTTPException
from models import ExpenseCreate
from services.expense_service import process_expense, get_recent_expenses

router = APIRouter()

@router.post("/{telegram_id}")
async def add_expense(telegram_id: int, expense: ExpenseCreate):
    try:
        result = await process_expense(
            telegram_id,
            expense.description,
            expense.amount,
            expense.category
        )
        if result["success"]:
            return result
        raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}")
async def get_expense_history(telegram_id: int, limit: int = 10):
    try:
        transactions = await get_recent_expenses(telegram_id, limit)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
