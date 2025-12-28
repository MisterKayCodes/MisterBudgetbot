from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime, timedelta

async def get_subscription(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    result = supabase.table("subscriptions").select("*").eq("user_id", user["id"]).order("created_at", desc=True).limit(1).maybeSingle().execute()

    return result.data

async def is_subscription_active(telegram_id: int):
    subscription = await get_subscription(telegram_id)

    if not subscription:
        return False

    if subscription["status"] != "active":
        return False

    if subscription.get("end_date"):
        end_date = datetime.fromisoformat(subscription["end_date"])
        if end_date < datetime.now():
            return False

    return True

async def redeem_trial_code(telegram_id: int, code: str):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return {"success": False, "message": "User not found"}

    supabase = get_supabase_client()

    trial_code = supabase.table("trial_codes").select("*").eq("code", code.upper()).eq("used", 0).maybeSingle().execute()

    if not trial_code.data:
        return {"success": False, "message": "Invalid or already used trial code"}

    now = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=trial_code.data["duration_days"])).isoformat()

    supabase.table("subscriptions").insert({
        "user_id": user["id"],
        "plan_type": "trial",
        "start_date": now,
        "end_date": end_date,
        "status": "active",
        "payment_method": "trial_code",
        "created_at": now
    }).execute()

    supabase.table("trial_codes").update({
        "used": 1,
        "used_by": user["id"],
        "used_at": now
    }).eq("code", code.upper()).execute()

    return {
        "success": True,
        "message": f"Trial activated! Valid for {trial_code.data['duration_days']} days."
    }
