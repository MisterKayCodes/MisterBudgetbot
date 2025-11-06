from database_models.users import get_user_by_telegram_id
from database import get_db
from utils.helpers import get_current_datetime

async def update_user_currency(telegram_id: int, currency: str) -> bool:
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        "UPDATE users SET currency = ?, updated_at = ? WHERE telegram_id = ?",
        (currency, now, telegram_id)
    )
    
    await db.commit()
    await db.close()
    
    return True

async def update_income_split(telegram_id: int, spending_pct: int, 
                              savings_pct: int, business_pct: int) -> bool:
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    if spending_pct + savings_pct + business_pct != 100:
        return False
    
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """UPDATE users SET spending_percent = ?, savings_percent = ?, 
           business_percent = ?, updated_at = ? WHERE telegram_id = ?""",
        (spending_pct, savings_pct, business_pct, now, telegram_id)
    )
    
    await db.commit()
    await db.close()
    
    return True

async def reset_user_data(telegram_id: int) -> bool:
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    db = await get_db()
    
    await db.execute("DELETE FROM transactions WHERE user_id = ?", (user['id'],))
    
    await db.execute("DELETE FROM goals WHERE user_id = ?", (user['id'],))
    
    await db.execute("UPDATE accounts SET balance = 0.0 WHERE user_id = ?", (user['id'],))
    
    await db.commit()
    await db.close()
    
    return True
