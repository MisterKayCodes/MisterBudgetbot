from database import get_supabase_client
from services.user_service import get_user_by_telegram_id

async def get_all_accounts(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return []

    supabase = get_supabase_client()
    result = supabase.table("accounts").select("*").eq("user_id", user["id"]).order("account_type").execute()

    return result.data

async def get_total_balance(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return 0.0

    supabase = get_supabase_client()
    result = supabase.table("accounts").select("balance").eq("user_id", user["id"]).neq("account_type", "main").execute()

    total = sum(account["balance"] for account in result.data)
    return total
