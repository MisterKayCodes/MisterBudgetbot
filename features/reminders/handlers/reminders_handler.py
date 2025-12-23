from aiogram import Router, F
from aiogram.types import CallbackQuery
from features.reminders.keyboards.reminders_keyboard import get_reminders_menu_keyboard, get_back_to_reminders_keyboard
from features.reminders.services.reminders_service import (
    get_user_reminders,
    toggle_daily_reminder,
    toggle_weekly_reminder
)

router = Router()

@router.callback_query(F.data == "menu:reminders")
async def show_reminders_menu(callback: CallbackQuery):
    reminders = await get_user_reminders(callback.from_user.id)
    
    daily_enabled = reminders['daily_enabled'] == 1 if reminders else False
    weekly_enabled = reminders['weekly_enabled'] == 1 if reminders else False
    
    text = f"""🗓️ Reminders & Notifications

Daily Reminder: {"🟢 Enabled" if daily_enabled else "🔴 Disabled"}
Weekly Report: {"🟢 Enabled" if weekly_enabled else "🔴 Disabled"}

Toggle reminders below:"""
    
    keyboard = get_reminders_menu_keyboard(daily_enabled, weekly_enabled)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "reminders:toggle_daily")
async def toggle_daily(callback: CallbackQuery):
    success = await toggle_daily_reminder(callback.from_user.id)
    
    if success:
        reminders = await get_user_reminders(callback.from_user.id)
        daily_enabled = reminders['daily_enabled'] == 1 if reminders else False
        weekly_enabled = reminders['weekly_enabled'] == 1 if reminders else False
        
        status = "enabled" if daily_enabled else "disabled"
        await callback.answer(f"Daily reminder {status}!")
        
        text = f"""🗓️ Reminders & Notifications

Daily Reminder: {"🟢 Enabled" if daily_enabled else "🔴 Disabled"}
Weekly Report: {"🟢 Enabled" if weekly_enabled else "🔴 Disabled"}

Toggle reminders below:"""
        
        keyboard = get_reminders_menu_keyboard(daily_enabled, weekly_enabled)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer("Error updating reminder", show_alert=True)

@router.callback_query(F.data == "reminders:toggle_weekly")
async def toggle_weekly(callback: CallbackQuery):
    success = await toggle_weekly_reminder(callback.from_user.id)
    
    if success:
        reminders = await get_user_reminders(callback.from_user.id)
        daily_enabled = reminders['daily_enabled'] == 1 if reminders else False
        weekly_enabled = reminders['weekly_enabled'] == 1 if reminders else False
        
        status = "enabled" if weekly_enabled else "disabled"
        await callback.answer(f"Weekly report {status}!")
        
        text = f"""🗓️ Reminders & Notifications

Daily Reminder: {"🟢 Enabled" if daily_enabled else "🔴 Disabled"}
Weekly Report: {"🟢 Enabled" if weekly_enabled else "🔴 Disabled"}

Toggle reminders below:"""
        
        keyboard = get_reminders_menu_keyboard(daily_enabled, weekly_enabled)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer("Error updating reminder", show_alert=True)
