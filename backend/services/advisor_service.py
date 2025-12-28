from database import get_supabase_client
from services.user_service import get_user_by_telegram_id
from datetime import datetime, timedelta

async def analyze_spending_habits(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()
    start_date = (datetime.now() - timedelta(days=30)).isoformat()

    transactions = supabase.table("transactions").select("*").eq("user_id", user["id"]).eq("transaction_type", "expense").gte("created_at", start_date).execute()

    total_expenses = sum(t["amount"] for t in transactions.data)

    category_analysis = {}
    for t in transactions.data:
        category = t.get("category", "General")
        if category not in category_analysis:
            category_analysis[category] = {"total": 0, "count": 0}
        category_analysis[category]["total"] += t["amount"]
        category_analysis[category]["count"] += 1

    categories = []
    for category, data in category_analysis.items():
        percentage = (data["total"] / total_expenses * 100) if total_expenses > 0 else 0
        categories.append({
            "category": category,
            "total": data["total"],
            "count": data["count"],
            "percentage": percentage
        })

    categories.sort(key=lambda x: x["total"], reverse=True)

    return {
        "total_expenses": total_expenses,
        "categories": categories,
        "top_category": categories[0] if categories else None
    }

async def analyze_savings_habits(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return None

    supabase = get_supabase_client()

    savings_account = supabase.table("accounts").select("*").eq("user_id", user["id"]).eq("account_type", "savings").maybeSingle().execute()
    savings_balance = savings_account.data["balance"] if savings_account.data else 0

    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    income_transactions = supabase.table("transactions").select("*").eq("user_id", user["id"]).eq("transaction_type", "income").gte("created_at", start_date).execute()

    total_income = sum(t["amount"] for t in income_transactions.data)

    goals = supabase.table("goals").select("*").eq("user_id", user["id"]).eq("status", "active").execute()

    total_goal_progress = sum(g["current_amount"] for g in goals.data)
    total_goal_target = sum(g["target_amount"] for g in goals.data)

    savings_rate = (savings_balance / total_income * 100) if total_income > 0 else 0

    return {
        "savings_balance": savings_balance,
        "total_income": total_income,
        "savings_rate": savings_rate,
        "active_goals": len(goals.data),
        "goal_progress": total_goal_progress,
        "goal_target": total_goal_target
    }

async def generate_recommendations(telegram_id: int):
    spending_analysis = await analyze_spending_habits(telegram_id)
    savings_analysis = await analyze_savings_habits(telegram_id)

    recommendations = []

    if spending_analysis and spending_analysis["top_category"] and spending_analysis["top_category"]["percentage"] > 40:
        recommendations.append(
            f"Your {spending_analysis['top_category']['category']} spending is {spending_analysis['top_category']['percentage']:.1f}% of total expenses. Consider reducing this category."
        )

    if savings_analysis:
        if savings_analysis["savings_rate"] < 15:
            recommendations.append(
                f"Your savings rate is {savings_analysis['savings_rate']:.1f}%. Aim for at least 20% to build wealth faster."
            )
        elif savings_analysis["savings_rate"] >= 20:
            recommendations.append(
                f"Great job! Your savings rate is {savings_analysis['savings_rate']:.1f}%. Keep it up!"
            )

        if savings_analysis["active_goals"] == 0:
            recommendations.append(
                "Set a savings goal to stay motivated and track your progress toward financial milestones."
            )

    if not recommendations:
        recommendations.append(
            "Your finances look healthy! Keep tracking and stay consistent."
        )

    return recommendations
