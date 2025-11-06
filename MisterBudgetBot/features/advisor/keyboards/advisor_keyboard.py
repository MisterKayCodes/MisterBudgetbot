from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_advisor_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Spending Analysis", callback_data="advisor:spending")],
        [InlineKeyboardButton(text="💰 Savings Analysis", callback_data="advisor:saving")],
        [InlineKeyboardButton(text="💡 Smart Recommendations", callback_data="advisor:recommendations")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_back_to_advisor_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Advisor", callback_data="menu:advisor")]
    ])
