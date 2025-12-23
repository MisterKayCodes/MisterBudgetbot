from database_models.users import get_user_by_telegram_id
from database_models.accounts import update_account_balance, get_account_by_type
from database_models.transactions import create_transaction

async def process_expense(telegram_id: int, name: str, amount: float, category: str = None):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False, "User not found"
    
    spending_account = await get_account_by_type(user['id'], 'spending')
    
    if not spending_account or spending_account['balance'] < amount:
        return False, "Insufficient balance in Spending Account"
    
    await update_account_balance(user['id'], 'spending', amount, 'subtract')
    
    await create_transaction(
        user['id'],
        'expense',
        amount,
        category or 'General',
        name,
        'spending'
    )
    
    return True, "Expense logged successfully"
