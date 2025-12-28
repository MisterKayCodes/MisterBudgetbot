from database import get_supabase_client
from datetime import datetime
import random
import string

async def toggle_subscription_mode():
    supabase = get_supabase_client()

    settings = supabase.table("admin_settings").select("*").eq("id", 1).maybeSingle().execute()

    if settings.data:
        new_mode = 0 if settings.data["subscription_mode"] == 1 else 1
        supabase.table("admin_settings").update({
            "subscription_mode": new_mode
        }).eq("id", 1).execute()
    else:
        supabase.table("admin_settings").insert({
            "id": 1,
            "subscription_mode": 1
        }).execute()
        new_mode = 1

    return new_mode

async def generate_trial_code(duration_days: int = 30):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    now = datetime.now().isoformat()

    supabase = get_supabase_client()

    supabase.table("trial_codes").insert({
        "code": code,
        "issued_by": None,
        "duration_days": duration_days,
        "used": 0,
        "used_by": None,
        "used_at": None,
        "created_at": now
    }).execute()

    return code

async def get_subscribers_list():
    supabase = get_supabase_client()

    result = supabase.table("subscriptions").select("*, users(full_name, email)").eq("status", "active").order("start_date", desc=True).execute()

    subscribers = []
    for row in result.data:
        subscribers.append({
            "full_name": row["users"]["full_name"],
            "email": row["users"]["email"],
            "plan_type": row["plan_type"],
            "start_date": row["start_date"],
            "end_date": row.get("end_date"),
            "status": row["status"]
        })

    return subscribers

async def get_bot_statistics():
    supabase = get_supabase_client()

    total_users = supabase.table("users").select("id", count="exact").execute()
    active_subs = supabase.table("subscriptions").select("id", count="exact").eq("status", "active").execute()
    total_txns = supabase.table("transactions").select("id", count="exact").execute()
    active_goals = supabase.table("goals").select("id", count="exact").eq("status", "active").execute()

    return {
        "total_users": total_users.count,
        "active_subscribers": active_subs.count,
        "total_transactions": total_txns.count,
        "active_goals": active_goals.count
    }

async def get_all_users():
    supabase = get_supabase_client()

    result = supabase.table("users").select("id, telegram_id, full_name, email, currency, created_at").order("created_at", desc=True).execute()

    return result.data

async def delete_all_users():
    supabase = get_supabase_client()

    supabase.table("pending_payments").delete().neq("id", 0).execute()
    supabase.table("subscriptions").delete().neq("id", 0).execute()
    supabase.table("reminders").delete().neq("id", 0).execute()
    supabase.table("goals").delete().neq("id", 0).execute()
    supabase.table("transactions").delete().neq("id", 0).execute()
    supabase.table("accounts").delete().neq("id", 0).execute()
    supabase.table("users").delete().neq("id", 0).execute()

    return True
