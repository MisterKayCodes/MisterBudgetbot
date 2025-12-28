from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard

router = Router()

def get_reminders_keyboard(daily_enabled: bool, weekly_enabled: bool) -> InlineKeyboardMarkup:
    daily_text = "Daily Reminder: ON" if daily_enabled else "Daily Reminder: OFF"
    weekly_text = "Weekly Report: ON" if weekly_enabled else "Weekly Report: OFF"

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=daily_text, callback_data="reminders:toggle_daily")],
        [InlineKeyboardButton(text=weekly_text, callback_data="reminders:toggle_weekly")],
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])

@router.callback_query(F.data == "menu:reminders")
async def show_reminders_menu(callback: CallbackQuery):
    try:
        reminders = await api_client.get_reminders(callback.from_user.id)

        daily_enabled = reminders.get('daily_enabled', 0) == 1
        weekly_enabled = reminders.get('weekly_enabled', 0) == 1

        text = f"""Reminders & Notifications

Daily Reminder: {"Enabled" if daily_enabled else "Disabled"}
Weekly Report: {"Enabled" if weekly_enabled else "Disabled"}

Toggle reminders below:"""

        await callback.message.edit_text(
            text,
            reply_markup=get_reminders_keyboard(daily_enabled, weekly_enabled)
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "reminders:toggle_daily")
async def toggle_daily(callback: CallbackQuery):
    try:
        result = await api_client.toggle_reminder(callback.from_user.id, "daily")

        daily_enabled = result.get('daily_enabled', 0) == 1
        weekly_enabled = result.get('weekly_enabled', 0) == 1

        status = "enabled" if daily_enabled else "disabled"
        await callback.answer(f"Daily reminder {status}!")

        text = f"""Reminders & Notifications

Daily Reminder: {"Enabled" if daily_enabled else "Disabled"}
Weekly Report: {"Enabled" if weekly_enabled else "Disabled"}

Toggle reminders below:"""

        await callback.message.edit_text(
            text,
            reply_markup=get_reminders_keyboard(daily_enabled, weekly_enabled)
        )

    except Exception as e:
        await callback.answer(f"Error: {str(e)}", show_alert=True)

@router.callback_query(F.data == "reminders:toggle_weekly")
async def toggle_weekly(callback: CallbackQuery):
    try:
        result = await api_client.toggle_reminder(callback.from_user.id, "weekly")

        daily_enabled = result.get('daily_enabled', 0) == 1
        weekly_enabled = result.get('weekly_enabled', 0) == 1

        status = "enabled" if weekly_enabled else "disabled"
        await callback.answer(f"Weekly report {status}!")

        text = f"""Reminders & Notifications

Daily Reminder: {"Enabled" if daily_enabled else "Disabled"}
Weekly Report: {"Enabled" if weekly_enabled else "Disabled"}

Toggle reminders below:"""

        await callback.message.edit_text(
            text,
            reply_markup=get_reminders_keyboard(daily_enabled, weekly_enabled)
        )

    except Exception as e:
        await callback.answer(f"Error: {str(e)}", show_alert=True)
