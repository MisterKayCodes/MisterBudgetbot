from database import get_db
from database_models.users import get_user_by_telegram_id
from utils.helpers import get_current_datetime
from datetime import datetime, timedelta

async def get_user_subscription(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return None
    
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM subscriptions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        (user['id'],)
    )
    subscription = await cursor.fetchone()
    await db.close()
    
    return subscription

async def redeem_trial_code(telegram_id: int, code: str):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False, "User not found"
    
    db = await get_db()
    
    cursor = await db.execute(
        "SELECT * FROM trial_codes WHERE code = ? AND used = 0",
        (code.upper(),)
    )
    trial_code = await cursor.fetchone()
    
    if not trial_code:
        await db.close()
        return False, "Invalid or already used trial code"
    
    now = get_current_datetime()
    end_date = (datetime.now() + timedelta(days=trial_code['duration_days'])).strftime('%Y-%m-%d %H:%M:%S')
    
    await db.execute(
        """INSERT INTO subscriptions (user_id, plan_type, start_date, end_date, 
           status, payment_method, created_at)
           VALUES (?, 'trial', ?, ?, 'active', 'trial_code', ?)""",
        (user['id'], now, end_date, now)
    )
    
    await db.execute(
        "UPDATE trial_codes SET used = 1, used_by = ?, used_at = ? WHERE code = ?",
        (user['id'], now, code.upper())
    )
    
    await db.commit()
    await db.close()
    
    return True, f"Trial activated! Valid for {trial_code['duration_days']} days."

async def is_subscription_active(telegram_id: int) -> bool:
    subscription = await get_user_subscription(telegram_id)
    
    if not subscription:
        return False
    
    if subscription['status'] != 'active':
        return False
    
    if subscription['end_date']:
        end_date = datetime.strptime(subscription['end_date'], '%Y-%m-%d %H:%M:%S')
        if end_date < datetime.now():
            return False
    
    return True
