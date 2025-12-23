from database import get_db
from utils.formatters import get_current_datetime
import config

async def create_user(telegram_id: int, full_name: str, email: str) -> int:
    db = await get_db()
    now = get_current_datetime()
    
    cursor = await db.execute(
        """INSERT INTO users (telegram_id, full_name, email, currency, 
           spending_percent, savings_percent, business_percent, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (telegram_id, full_name, email, config.DEFAULT_CURRENCY,
         config.DEFAULT_SPENDING_PERCENT, config.DEFAULT_SAVINGS_PERCENT,
         config.DEFAULT_BUSINESS_PERCENT, now, now)
    )
    
    user_id = cursor.lastrowid
    await db.commit()
    
    await create_default_accounts(user_id)
    
    await db.close()
    return user_id

async def create_default_accounts(user_id: int):
    db = await get_db()
    now = get_current_datetime()
    
    account_types = [
        ("main", "Main Account"),
        ("spending", "Spending"),
        ("savings", "Savings"),
        ("business", "Business")
    ]
    
    for acc_type, acc_name in account_types:
        await db.execute(
            """INSERT INTO accounts (user_id, account_type, account_name, balance, created_at, updated_at)
               VALUES (?, ?, ?, 0.0, ?, ?)""",
            (user_id, acc_type, acc_name, now, now)
        )
    
    await db.commit()
    await db.close()

async def get_user_by_telegram_id(telegram_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    user = await cursor.fetchone()
    await db.close()
    return user

async def update_user_settings(user_id: int, **kwargs):
    db = await get_db()
    now = get_current_datetime()
    
    fields = []
    values = []
    
    for key, value in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(value)
    
    fields.append("updated_at = ?")
    values.append(now)
    values.append(user_id)
    
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    await db.execute(query, values)
    await db.commit()
    await db.close()
