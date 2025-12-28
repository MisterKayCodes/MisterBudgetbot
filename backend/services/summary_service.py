from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime, timedelta
import csv
import io

async def get_period_summary(telegram_id: int, days: int = None):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()

    if days:
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        transactions = supabase.table("transactions").select("*").eq("user_id", user["id"]).gte("created_at", start_date).execute()
    else:
        transactions = supabase.table("transactions").select("*").eq("user_id", user["id"]).execute()

    income_total = sum(t["amount"] for t in transactions.data if t["transaction_type"] == "income")
    expense_total = sum(t["amount"] for t in transactions.data if t["transaction_type"] == "expense")

    expense_by_category = {}
    for t in transactions.data:
        if t["transaction_type"] == "expense":
            category = t.get("category", "General")
            if category not in expense_by_category:
                expense_by_category[category] = {"total": 0, "count": 0}
            expense_by_category[category]["total"] += t["amount"]
            expense_by_category[category]["count"] += 1

    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "net": income_total - expense_total,
        "expense_by_category": expense_by_category,
        "transaction_count": len(transactions.data)
    }

async def generate_csv_export(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    transactions = supabase.table("transactions").select("*").eq("user_id", user["id"]).order("created_at", desc=True).execute()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Date", "Type", "Amount", "Category", "Description"])

    for txn in transactions.data:
        writer.writerow([
            txn["created_at"],
            txn["transaction_type"].capitalize(),
            txn["amount"],
            txn.get("category", ""),
            txn.get("description", "")
        ])

    csv_content = output.getvalue()
    output.close()

    return csv_content
