from database_models.goals import create_goal, get_active_goals, get_completed_goals
from database_models.users import get_user_by_telegram_id

async def add_new_goal(telegram_id: int, goal_name: str, target_amount: float, 
                      deadline: str = None, auto_save_percent: int = 0):
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return False
    
    await create_goal(user['id'], goal_name, target_amount, deadline, auto_save_percent)
    return True
