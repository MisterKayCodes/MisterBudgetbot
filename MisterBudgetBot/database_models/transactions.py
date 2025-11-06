from database import get_db
from utils.formatters import get_current_datetime
from datetime import datetime, timedelta
from typing import Optional

async def create_transaction(user_id: int, transaction_type: str, amount: float, 
                            category: Optional[str] = None, description: Optional[str] = None, 
                            account_type: Optional[str] = None):
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """INSERT INTO transactions (user_id, transaction_type, amount, category, 
           description, account_type, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, transaction_type, amount, category, description, account_type, now)
    )
    
    await db.commit()
    await db.close()

async def get_recent_transactions(user_id: int, transaction_type: Optional[str] = None, limit: int = 10):
    db = await get_db()
    
    if transaction_type:
        cursor = await db.execute(
            """SELECT * FROM transactions WHERE user_id = ? AND transaction_type = ?
               ORDER BY created_at DESC LIMIT ?""",
            (user_id, transaction_type, limit)
        )
    else:
        cursor = await db.execute(
            """SELECT * FROM transactions WHERE user_id = ?
               ORDER BY created_at DESC LIMIT ?""",
            (user_id, limit)
        )
    
    transactions = await cursor.fetchall()
    await db.close()
    return transactions

async def get_monthly_expenses(user_id: int) -> float:
    db = await get_db()
    now = datetime.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    cursor = await db.execute(
        """SELECT SUM(amount) as total FROM transactions 
           WHERE user_id = ? AND transaction_type = 'expense' AND created_at >= ?""",
        (user_id, first_day.isoformat())
    )
    
    result = await cursor.fetchone()
    await db.close()
    return result['total'] if result['total'] else 0.0

async def get_transactions_by_period(user_id: int, days: int):
    db = await get_db()
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    cursor = await db.execute(
        """SELECT * FROM transactions WHERE user_id = ? AND created_at >= ?
           ORDER BY created_at DESC""",
        (user_id, cutoff_date)
    )
    
    transactions = await cursor.fetchall()
    await db.close()
    return transactions
