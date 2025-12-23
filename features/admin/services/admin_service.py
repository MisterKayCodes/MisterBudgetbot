from database import get_db
from utils.helpers import get_current_datetime
import random
import string

async def toggle_subscription_mode():
    db = await get_db()
    
    cursor = await db.execute("SELECT subscription_mode FROM admin_settings WHERE id = 1")
    settings = await cursor.fetchone()
    
    if settings:
        new_mode = 0 if settings['subscription_mode'] == 1 else 1
        await db.execute(
            "UPDATE admin_settings SET subscription_mode = ? WHERE id = 1",
            (new_mode,)
        )
    else:
        await db.execute(
            "INSERT INTO admin_settings (id, subscription_mode) VALUES (1, 1)"
        )
        new_mode = 1
    
    await db.commit()
    await db.close()
    
    return new_mode

async def generate_trial_code(duration_days: int = 30):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    now = get_current_datetime()
    
    db = await get_db()
    
    await db.execute(
        """INSERT INTO trial_codes (code, issued_by, duration_days, used, used_by, used_at, created_at)
           VALUES (?, NULL, ?, 0, NULL, NULL, ?)""",
        (code, duration_days, now)
    )
    
    await db.commit()
    await db.close()
    
    return code

async def get_subscribers_list():
    db = await get_db()
    
    query = """
        SELECT u.full_name, u.email, s.plan_type, s.start_date, s.end_date, s.status
        FROM subscriptions s
        JOIN users u ON s.user_id = u.id
        WHERE s.status = 'active'
        ORDER BY s.start_date DESC
    """
    cursor = await db.execute(query)
    rows = await cursor.fetchall()
    await db.close()
    
    subscribers = []
    for row in rows:
        # Assuming row columns are in order: full_name, email, plan_type, start_date, end_date, status
        subscribers.append({
            "full_name": row[0],
            "email": row[1],
            "plan_type": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "status": row[5]
        })
    
    return subscribers

async def get_bot_statistics():
    db = await get_db()
    
    total_users_cursor = await db.execute("SELECT COUNT(*) as count FROM users")
    total_users = await total_users_cursor.fetchone()
    
    active_subs_cursor = await db.execute(
        "SELECT COUNT(*) as count FROM subscriptions WHERE status = 'active'"
    )
    active_subs = await active_subs_cursor.fetchone()
    
    total_txns_cursor = await db.execute("SELECT COUNT(*) as count FROM transactions")
    total_txns = await total_txns_cursor.fetchone()
    
    total_goals_cursor = await db.execute("SELECT COUNT(*) as count FROM goals WHERE status = 'active'")
    total_goals = await total_goals_cursor.fetchone()
    
    await db.close()
    
    return {
        'total_users': total_users['count'] if total_users else 0,
        'active_subscribers': active_subs['count'] if active_subs else 0,
        'total_transactions': total_txns['count'] if total_txns else 0,
        'active_goals': total_goals['count'] if total_goals else 0
    }

async def get_all_users():
    db = await get_db()
    
    query = """
        SELECT id, telegram_id, full_name, email, currency, created_at
        FROM users
        ORDER BY created_at DESC
    """
    cursor = await db.execute(query)
    rows = await cursor.fetchall()
    await db.close()
    
    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "telegram_id": row[1],
            "full_name": row[2],
            "email": row[3],
            "currency": row[4],
            "created_at": row[5]
        })
    
    return users

async def delete_all_users():
    db = await get_db()
    
    # Delete all related data first due to foreign key constraints
    await db.execute("DELETE FROM pending_payments")
    await db.execute("DELETE FROM subscriptions")
    await db.execute("DELETE FROM trial_codes WHERE used = 1")
    await db.execute("DELETE FROM reminders")
    await db.execute("DELETE FROM goals")
    await db.execute("DELETE FROM transactions")
    await db.execute("DELETE FROM accounts")
    await db.execute("DELETE FROM users")
    
    await db.commit()
    await db.close()
    
    return True
