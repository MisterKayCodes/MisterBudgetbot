from database import get_db
from database_models.accounts import get_account_by_type
from datetime import datetime, timedelta

async def analyze_spending_habits(user_id: int):
    db = await get_db()
    
    cursor = await db.execute(
        """SELECT category, SUM(amount) as total, COUNT(*) as count
           FROM transactions 
           WHERE user_id = ? AND transaction_type = 'expense' AND created_at >= ?
           GROUP BY category
           ORDER BY total DESC""",
        (user_id, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'))
    )
    
    categories = await cursor.fetchall()
    
    total_cursor = await db.execute(
        """SELECT SUM(amount) as total FROM transactions 
           WHERE user_id = ? AND transaction_type = 'expense' AND created_at >= ?""",
        (user_id, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'))
    )
    total_row = await total_cursor.fetchone()
    total_expenses = total_row['total'] if total_row['total'] else 0
    
    await db.close()
    
    category_analysis = []
    for cat in categories:
        percentage = (cat['total'] / total_expenses * 100) if total_expenses > 0 else 0
        category_analysis.append({
            'category': cat['category'],
            'total': cat['total'],
            'count': cat['count'],
            'percentage': percentage
        })
    
    return {
        'total_expenses': total_expenses,
        'categories': category_analysis,
        'top_category': category_analysis[0] if category_analysis else None
    }

async def analyze_savings_habits(user_id: int):
    savings_account = await get_account_by_type(user_id, 'savings')
    savings_balance = savings_account['balance'] if savings_account else 0
    
    db = await get_db()
    
    cursor = await db.execute(
        """SELECT SUM(amount) as total FROM transactions 
           WHERE user_id = ? AND transaction_type = 'income' AND created_at >= ?""",
        (user_id, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'))
    )
    income_row = await cursor.fetchone()
    total_income = income_row['total'] if income_row['total'] else 0
    
    cursor = await db.execute(
        """SELECT current_amount, target_amount FROM goals 
           WHERE user_id = ? AND status = 'active'""",
        (user_id,)
    )
    goals = await cursor.fetchall()
    
    await db.close()
    
    total_goal_progress = sum(g['current_amount'] for g in goals)
    total_goal_target = sum(g['target_amount'] for g in goals)
    
    savings_rate = (savings_balance / total_income * 100) if total_income > 0 else 0
    
    return {
        'savings_balance': savings_balance,
        'total_income': total_income,
        'savings_rate': savings_rate,
        'active_goals': len(goals),
        'goal_progress': total_goal_progress,
        'goal_target': total_goal_target
    }

async def generate_recommendations(user_id: int):
    spending_analysis = await analyze_spending_habits(user_id)
    savings_analysis = await analyze_savings_habits(user_id)
    
    recommendations = []
    
    if spending_analysis['top_category'] and spending_analysis['top_category']['percentage'] > 40:
        recommendations.append(
            f"🔴 Your {spending_analysis['top_category']['category']} spending is {spending_analysis['top_category']['percentage']:.1f}% of total expenses. Consider reducing this category."
        )
    
    if savings_analysis['savings_rate'] < 15:
        recommendations.append(
            f"🟡 Your savings rate is {savings_analysis['savings_rate']:.1f}%. Aim for at least 20% to build wealth faster."
        )
    elif savings_analysis['savings_rate'] >= 20:
        recommendations.append(
            f"🟢 Great job! Your savings rate is {savings_analysis['savings_rate']:.1f}%. Keep it up!"
        )
    
    if savings_analysis['active_goals'] == 0:
        recommendations.append(
            "💡 Set a savings goal to stay motivated and track your progress toward financial milestones."
        )
    
    if not recommendations:
        recommendations.append(
            "🎉 Your finances look healthy! Keep tracking and stay consistent."
        )
    
    return recommendations
