from database import get_supabase_client
from config import settings
from datetime import datetime

async def create_user(telegram_id: int, full_name: str, email: str):
    supabase = get_supabase_client()

    existing = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
    if existing.data:
        return None

    now = datetime.now().isoformat()

    user_data = {
        "telegram_id": telegram_id,
        "full_name": full_name,
        "email": email,
        "currency": settings.default_currency,
        "spending_percent": settings.default_spending_percent,
        "savings_percent": settings.default_savings_percent,
        "business_percent": settings.default_business_percent,
        "created_at": now,
        "updated_at": now
    }

    result = supabase.table("users").insert(user_data).execute()

    if result.data:
        user_id = result.data[0]["id"]

        account_types = [
            ("main", "Main Account"),
            ("spending", "Spending"),
            ("savings", "Savings"),
            ("business", "Business")
        ]

        for acc_type, acc_name in account_types:
            supabase.table("accounts").insert({
                "user_id": user_id,
                "account_type": acc_type,
                "account_name": acc_name,
                "balance": 0.0,
                "created_at": now,
                "updated_at": now
            }).execute()

        return result.data[0]

    return None

async def get_user_by_telegram_id(telegram_id: int):
    supabase = get_supabase_client()
    result = supabase.table("users").select("*").eq("telegram_id", telegram_id).maybeSingle().execute()
    return result.data

async def update_user_settings(telegram_id: int, updates: dict):
    supabase = get_supabase_client()

    updates["updated_at"] = datetime.now().isoformat()

    result = supabase.table("users").update(updates).eq("telegram_id", telegram_id).execute()

    if result.data:
        return result.data[0]
    return None
