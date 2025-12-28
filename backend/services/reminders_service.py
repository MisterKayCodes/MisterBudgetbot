from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime

async def get_reminders(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()

    daily = supabase.table("reminders").select("*").eq("user_id", user["id"]).eq("reminder_type", "daily").maybeSingle().execute()
    weekly = supabase.table("reminders").select("*").eq("user_id", user["id"]).eq("reminder_type", "weekly").maybeSingle().execute()

    return {
        "daily_enabled": daily.data["enabled"] if daily.data else 0,
        "weekly_enabled": weekly.data["enabled"] if weekly.data else 0
    }

async def toggle_reminder(telegram_id: int, reminder_type: str):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    now = datetime.now().isoformat()

    reminder = supabase.table("reminders").select("*").eq("user_id", user["id"]).eq("reminder_type", reminder_type).maybeSingle().execute()

    if reminder.data:
        new_status = 0 if reminder.data["enabled"] == 1 else 1
        supabase.table("reminders").update({
            "enabled": new_status,
            "updated_at": now
        }).eq("user_id", user["id"]).eq("reminder_type", reminder_type).execute()
    else:
        supabase.table("reminders").insert({
            "user_id": user["id"],
            "reminder_type": reminder_type,
            "enabled": 1,
            "created_at": now,
            "updated_at": now
        }).execute()

    return await get_reminders(telegram_id)
