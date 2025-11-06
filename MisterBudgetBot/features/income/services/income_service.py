from database_models.users import get_user_by_telegram_id
from database_models.accounts import update_account_balance
from database_models.transactions import create_transaction
from database_models.goals import get_active_goals, update_goal_progress
from utils.helpers import split_income

async def process_income(telegram_id: int, amount: float):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return None
    
    splits = split_income(
        amount,
        user['spending_percent'],
        user['savings_percent'],
        user['business_percent']
    )
    
    await update_account_balance(user['id'], 'spending', splits['spending'], 'add')
    await update_account_balance(user['id'], 'savings', splits['savings'], 'add')
    await update_account_balance(user['id'], 'business', splits['business'], 'add')
    
    await create_transaction(
        user['id'],
        'income',
        amount,
        'Income',
        f"Split: {user['spending_percent']}% Spending, {user['savings_percent']}% Savings, {user['business_percent']}% Business"
    )
    
    active_goals = await get_active_goals(user['id'])
    for goal in active_goals:
        if goal['auto_save_percent'] > 0:
            goal_amount = amount * goal['auto_save_percent'] / 100
            await update_goal_progress(goal['id'], goal_amount)
    
    return splits
