from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime

async def create_goal(telegram_id: int, goal_name: str, target_amount: float, deadline: str = None, auto_save_percent: int = 0):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    now = datetime.now().isoformat()

    goal_data = {
        "user_id": user["id"],
        "goal_name": goal_name,
        "target_amount": target_amount,
        "current_amount": 0.0,
        "auto_save_percent": auto_save_percent,
        "deadline": deadline,
        "status": "active",
        "created_at": now,
        "updated_at": now
    }

    result = supabase.table("goals").insert(goal_data).execute()

    if result.data:
        return result.data[0]
    return None

async def get_active_goals(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return []

    supabase = get_supabase_client()
    result = supabase.table("goals").select("*").eq("user_id", user["id"]).eq("status", "active").order("created_at", desc=True).execute()

    return result.data

async def get_completed_goals(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return []

    supabase = get_supabase_client()
    result = supabase.table("goals").select("*").eq("user_id", user["id"]).eq("status", "completed").order("updated_at", desc=True).execute()

    return result.data

async def update_goal_progress(goal_id: int, amount: float):
    supabase = get_supabase_client()
    now = datetime.now().isoformat()

    goal = supabase.table("goals").select("*").eq("id", goal_id).maybeSingle().execute()

    if not goal.data:
        return False

    new_current = goal.data["current_amount"] + amount
    status = "completed" if new_current >= goal.data["target_amount"] else "active"

    supabase.table("goals").update({
        "current_amount": new_current,
        "status": status,
        "updated_at": now
    }).eq("id", goal_id).execute()

    return True
