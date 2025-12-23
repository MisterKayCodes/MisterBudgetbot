from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_income_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add Income", callback_data="income:add")],
        [InlineKeyboardButton(text="📂 View Recent Incomes", callback_data="income:recent")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_back_to_income_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Income Menu", callback_data="menu:add_income")],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu:main")]
    ])
