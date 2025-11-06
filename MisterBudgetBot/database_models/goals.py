from database import get_db
from utils.formatters import get_current_datetime

async def create_goal(user_id: int, goal_name: str, target_amount: float, 
                     deadline: str = None, auto_save_percent: int = 0):
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """INSERT INTO goals (user_id, goal_name, target_amount, current_amount, 
           auto_save_percent, deadline, status, created_at, updated_at)
           VALUES (?, ?, ?, 0.0, ?, ?, 'active', ?, ?)""",
        (user_id, goal_name, target_amount, auto_save_percent, deadline, now, now)
    )
    
    await db.commit()
    await db.close()

async def get_active_goals(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        """SELECT * FROM goals WHERE user_id = ? AND status = 'active'
           ORDER BY created_at DESC""",
        (user_id,)
    )
    goals = await cursor.fetchall()
    await db.close()
    return goals

async def get_completed_goals(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        """SELECT * FROM goals WHERE user_id = ? AND status = 'completed'
           ORDER BY updated_at DESC""",
        (user_id,)
    )
    goals = await cursor.fetchall()
    await db.close()
    return goals

async def update_goal_progress(goal_id: int, amount: float):
    db = await get_db()
    now = get_current_datetime()
    
    await db.execute(
        """UPDATE goals SET current_amount = current_amount + ?, updated_at = ?
           WHERE id = ?""",
        (amount, now, goal_id)
    )
    
    cursor = await db.execute(
        "SELECT current_amount, target_amount FROM goals WHERE id = ?",
        (goal_id,)
    )
    goal = await cursor.fetchone()
    
    if goal and goal['current_amount'] >= goal['target_amount']:
        await db.execute(
            "UPDATE goals SET status = 'completed', updated_at = ? WHERE id = ?",
            (now, goal_id)
        )
    
    await db.commit()
    await db.close()

async def get_goal_by_id(goal_id: int):
    db = await get_db()
    cursor = await db.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    goal = await cursor.fetchone()
    await db.close()
    return goal
