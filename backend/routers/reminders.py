from fastapi import APIRouter, HTTPException
from models import ReminderToggle
from services.reminders_service import get_reminders, toggle_reminder

router = APIRouter()

@router.get("/{telegram_id}")
async def get_user_reminders(telegram_id: int):
    try:
        reminders = await get_reminders(telegram_id)
        return reminders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{telegram_id}/toggle")
async def toggle_user_reminder(telegram_id: int, reminder: ReminderToggle):
    try:
        result = await toggle_reminder(telegram_id, reminder.reminder_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
