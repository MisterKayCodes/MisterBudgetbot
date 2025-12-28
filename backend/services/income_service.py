from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime

async def process_income(telegram_id: int, amount: float):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    now = datetime.now().isoformat()

    spending_amount = round(amount * user["spending_percent"] / 100, 2)
    savings_amount = round(amount * user["savings_percent"] / 100, 2)
    business_amount = round(amount * user["business_percent"] / 100, 2)

    supabase.table("accounts").update({
        "balance": supabase.table("accounts").select("balance").eq("user_id", user["id"]).eq("account_type", "spending").maybeSingle().execute().data["balance"] + spending_amount,
        "updated_at": now
    }).eq("user_id", user["id"]).eq("account_type", "spending").execute()

    supabase.table("accounts").update({
        "balance": supabase.table("accounts").select("balance").eq("user_id", user["id"]).eq("account_type", "savings").maybeSingle().execute().data["balance"] + savings_amount,
        "updated_at": now
    }).eq("user_id", user["id"]).eq("account_type", "savings").execute()

    supabase.table("accounts").update({
        "balance": supabase.table("accounts").select("balance").eq("user_id", user["id"]).eq("account_type", "business").maybeSingle().execute().data["balance"] + business_amount,
        "updated_at": now
    }).eq("user_id", user["id"]).eq("account_type", "business").execute()

    supabase.table("transactions").insert({
        "user_id": user["id"],
        "transaction_type": "income",
        "amount": amount,
        "category": "Income",
        "description": f"Split: {user['spending_percent']}% Spending, {user['savings_percent']}% Savings, {user['business_percent']}% Business",
        "created_at": now
    }).execute()

    goals = supabase.table("goals").select("*").eq("user_id", user["id"]).eq("status", "active").execute()

    goal_allocations = []
    for goal in goals.data:
        if goal["auto_save_percent"] > 0:
            goal_amount = amount * goal["auto_save_percent"] / 100

            new_current = goal["current_amount"] + goal_amount
            status = "completed" if new_current >= goal["target_amount"] else "active"

            supabase.table("goals").update({
                "current_amount": new_current,
                "status": status,
                "updated_at": now
            }).eq("id", goal["id"]).execute()

            goal_allocations.append({
                "goal_name": goal["goal_name"],
                "amount": goal_amount,
                "percent": goal["auto_save_percent"]
            })

    return {
        "success": True,
        "amount": amount,
        "splits": {
            "spending": spending_amount,
            "savings": savings_amount,
            "business": business_amount
        },
        "goal_allocations": goal_allocations
    }

async def get_recent_income(telegram_id: int, limit: int = 10):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return []

    supabase = get_supabase_client()
    result = supabase.table("transactions").select("*").eq("user_id", user["id"]).eq("transaction_type", "income").order("created_at", desc=True).limit(limit).execute()

    return result.data
