from database import get_db
from database_models.users import get_user_by_telegram_id
from utils.helpers import get_current_datetime

async def get_user_reminders(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return None
    
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ? AND reminder_type = 'daily'",
        (user['id'],)
    )
    daily_reminder = await cursor.fetchone()
    
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ? AND reminder_type = 'weekly'",
        (user['id'],)
    )
    weekly_reminder = await cursor.fetchone()
    
    await db.close()
    
    return {
        'daily_enabled': daily_reminder['enabled'] if daily_reminder else 0,
        'weekly_enabled': weekly_reminder['enabled'] if weekly_reminder else 0
    }

async def toggle_daily_reminder(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    db = await get_db()
    now = get_current_datetime()
    
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ? AND reminder_type = 'daily'",
        (user['id'],)
    )
    reminder = await cursor.fetchone()
    
    if reminder:
        new_status = 0 if reminder['enabled'] == 1 else 1
        await db.execute(
            "UPDATE reminders SET enabled = ?, updated_at = ? WHERE user_id = ? AND reminder_type = 'daily'",
            (new_status, now, user['id'])
        )
    else:
        await db.execute(
            "INSERT INTO reminders (user_id, reminder_type, enabled, created_at, updated_at) VALUES (?, 'daily', 1, ?, ?)",
            (user['id'], now, now)
        )
    
    await db.commit()
    await db.close()
    
    return True

async def toggle_weekly_reminder(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    db = await get_db()
    now = get_current_datetime()
    
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ? AND reminder_type = 'weekly'",
        (user['id'],)
    )
    reminder = await cursor.fetchone()
    
    if reminder:
        new_status = 0 if reminder['enabled'] == 1 else 1
        await db.execute(
            "UPDATE reminders SET enabled = ?, updated_at = ? WHERE user_id = ? AND reminder_type = 'weekly'",
            (new_status, now, user['id'])
        )
    else:
        await db.execute(
            "INSERT INTO reminders (user_id, reminder_type, enabled, created_at, updated_at) VALUES (?, 'weekly', 1, ?, ?)",
            (user['id'], now, now)
        )
    
    await db.commit()
    await db.close()
    
    return True
