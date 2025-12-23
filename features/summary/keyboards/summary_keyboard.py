from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_summary_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Weekly Report", callback_data="summary:weekly")],
        [InlineKeyboardButton(text="📆 Monthly Report", callback_data="summary:monthly")],
        [InlineKeyboardButton(text="📊 All Time Stats", callback_data="summary:alltime")],
        [InlineKeyboardButton(text="📥 Export CSV", callback_data="summary:export")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_back_to_summary_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Summary", callback_data="menu:summary")]
    ])
