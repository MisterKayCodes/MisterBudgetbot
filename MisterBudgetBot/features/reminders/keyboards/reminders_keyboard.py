from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_reminders_menu_keyboard(daily_enabled: bool, weekly_enabled: bool) -> InlineKeyboardMarkup:
    daily_text = "🔔 Daily Reminder: ON" if daily_enabled else "🔕 Daily Reminder: OFF"
    weekly_text = "📅 Weekly Report: ON" if weekly_enabled else "📅 Weekly Report: OFF"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=daily_text, callback_data="reminders:toggle_daily")],
        [InlineKeyboardButton(text=weekly_text, callback_data="reminders:toggle_weekly")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_back_to_reminders_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Reminders", callback_data="menu:reminders")]
    ])
