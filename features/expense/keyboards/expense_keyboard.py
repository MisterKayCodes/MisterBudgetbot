from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_expense_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Log New Expense", callback_data="expense:add")],
        [InlineKeyboardButton(text="📂 View Recent Expenses", callback_data="expense:recent")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🍔 Food", callback_data="expense:cat:Food"),
            InlineKeyboardButton(text="🚗 Transport", callback_data="expense:cat:Transport")
        ],
        [
            InlineKeyboardButton(text="🏠 Housing", callback_data="expense:cat:Housing"),
            InlineKeyboardButton(text="🎉 Entertainment", callback_data="expense:cat:Entertainment")
        ],
        [
            InlineKeyboardButton(text="🛒 Shopping", callback_data="expense:cat:Shopping"),
            InlineKeyboardButton(text="💊 Health", callback_data="expense:cat:Health")
        ],
        [InlineKeyboardButton(text="⏭️ Skip Category", callback_data="expense:cat:General")]
    ])

def get_back_to_expense_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Expense Menu", callback_data="menu:add_expense")],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu:main")]
    ])
