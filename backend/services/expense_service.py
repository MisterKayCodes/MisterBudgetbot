from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime

async def process_expense(telegram_id: int, description: str, amount: float, category: str):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return {"success": False, "message": "User not found"}

    supabase = get_supabase_client()

    spending_account = supabase.table("accounts").select("*").eq("user_id", user["id"]).eq("account_type", "spending").maybeSingle().execute()

    if not spending_account.data or spending_account.data["balance"] < amount:
        return {"success": False, "message": "Insufficient balance in Spending Account"}

    now = datetime.now().isoformat()

    supabase.table("accounts").update({
        "balance": spending_account.data["balance"] - amount,
        "updated_at": now
    }).eq("user_id", user["id"]).eq("account_type", "spending").execute()

    supabase.table("transactions").insert({
        "user_id": user["id"],
        "transaction_type": "expense",
        "amount": amount,
        "category": category,
        "description": description,
        "account_type": "spending",
        "created_at": now
    }).execute()

    return {
        "success": True,
        "message": "Expense logged successfully",
        "amount": amount,
        "category": category,
        "description": description
    }

async def get_recent_expenses(telegram_id: int, limit: int = 10):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return []

    supabase = get_supabase_client()
    result = supabase.table("transactions").select("*").eq("user_id", user["id"]).eq("transaction_type", "expense").order("created_at", desc=True).limit(limit).execute()

    return result.data
