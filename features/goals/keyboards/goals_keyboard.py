from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_goals_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Create New Goal", callback_data="goals:create")],
        [InlineKeyboardButton(text="📈 View Active Goals", callback_data="goals:active")],
        [InlineKeyboardButton(text="✅ Completed Goals", callback_data="goals:completed")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_skip_deadline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭️ Skip Deadline", callback_data="goals:skip_deadline")]
    ])

def get_back_to_goals_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Goals Menu", callback_data="menu:goals")],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu:main")]
    ])
