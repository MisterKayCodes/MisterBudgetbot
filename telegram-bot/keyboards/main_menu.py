from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Add Income", callback_data="menu:add_income"),
            InlineKeyboardButton(text="Add Expense", callback_data="menu:add_expense")
        ],
        [
            InlineKeyboardButton(text="My Goals", callback_data="menu:goals"),
            InlineKeyboardButton(text="Advisor", callback_data="menu:advisor")
        ],
        [
            InlineKeyboardButton(text="Summary", callback_data="menu:summary"),
            InlineKeyboardButton(text="Settings", callback_data="menu:settings")
        ],
        [
            InlineKeyboardButton(text="Accounts", callback_data="menu:accounts"),
            InlineKeyboardButton(text="Reminders", callback_data="menu:reminders")
        ]
    ])

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])
