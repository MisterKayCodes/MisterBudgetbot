from database import get_db
from utils.formatters import get_current_datetime

async def get_user_accounts(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM accounts WHERE user_id = ? ORDER BY account_type",
        (user_id,)
    )
    accounts = await cursor.fetchall()
    await db.close()
    return accounts

async def get_account_by_type(user_id: int, account_type: str):
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM accounts WHERE user_id = ? AND account_type = ?",
        (user_id, account_type)
    )
    account = await cursor.fetchone()
    await db.close()
    return account

async def update_account_balance(user_id: int, account_type: str, amount: float, operation: str = "add"):
    db = await get_db()
    now = get_current_datetime()
    
    if operation == "add":
        await db.execute(
            """UPDATE accounts SET balance = balance + ?, updated_at = ?
               WHERE user_id = ? AND account_type = ?""",
            (amount, now, user_id, account_type)
        )
    elif operation == "subtract":
        await db.execute(
            """UPDATE accounts SET balance = balance - ?, updated_at = ?
               WHERE user_id = ? AND account_type = ?""",
            (amount, now, user_id, account_type)
        )
    elif operation == "set":
        await db.execute(
            """UPDATE accounts SET balance = ?, updated_at = ?
               WHERE user_id = ? AND account_type = ?""",
            (amount, now, user_id, account_type)
        )
    
    await db.commit()
    await db.close()

async def rename_account(user_id: int, account_type: str, new_name: str):
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """UPDATE accounts SET account_name = ?, updated_at = ?
           WHERE user_id = ? AND account_type = ?""",
        (new_name, now, user_id, account_type)
    )
    
    await db.commit()
    await db.close()

async def get_total_balance(user_id: int) -> float:
    db = await get_db()
    cursor = await db.execute(
        "SELECT SUM(balance) as total FROM accounts WHERE user_id = ? AND account_type != 'main'",
        (user_id,)
    )
    result = await cursor.fetchone()
    await db.close()
    return result['total'] if result['total'] else 0.0
