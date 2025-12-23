from database import get_db
from utils.formatters import get_current_datetime

async def get_user_reminders(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ?",
        (user_id,)
    )
    reminders = await cursor.fetchall()
    await db.close()
    return reminders

async def toggle_reminder(user_id: int, reminder_type: str):
    db = await get_db()
    now = get_current_datetime()
    
    cursor = await db.execute(
        "SELECT * FROM reminders WHERE user_id = ? AND reminder_type = ?",
        (user_id, reminder_type)
    )
    reminder = await cursor.fetchone()
    
    if reminder:
        new_status = 0 if reminder['enabled'] else 1
        await db.execute(
            "UPDATE reminders SET enabled = ?, updated_at = ? WHERE id = ?",
            (new_status, now, reminder['id'])
        )
    else:
        await db.execute(
            """INSERT INTO reminders (user_id, reminder_type, enabled, created_at, updated_at)
               VALUES (?, ?, 1, ?, ?)""",
            (user_id, reminder_type, now, now)
        )
    
    await db.commit()
    await db.close()

async def update_reminder_time(user_id: int, reminder_type: str, time: str):
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """UPDATE reminders SET time = ?, updated_at = ?
           WHERE user_id = ? AND reminder_type = ?""",
        (time, now, user_id, reminder_type)
    )
    
    await db.commit()
    await db.close()
