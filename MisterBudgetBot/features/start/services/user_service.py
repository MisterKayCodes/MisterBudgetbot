from database_models.users import create_user, get_user_by_telegram_id

async def get_or_create_user(telegram_id: int, full_name: str = None, email: str = None):
    user = await get_user_by_telegram_id(telegram_id)
    
    if user:
        return user
    
    if full_name and email:
        user_id = await create_user(telegram_id, full_name, email)
        return await get_user_by_telegram_id(telegram_id)
    
    return None
