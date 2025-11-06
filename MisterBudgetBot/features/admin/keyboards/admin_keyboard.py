from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Toggle Subscription Mode", callback_data="admin:toggle_sub")],
        [InlineKeyboardButton(text="🎟️ Generate Trial Code", callback_data="admin:trial")],
        [InlineKeyboardButton(text="📋 View Subscribers", callback_data="admin:subscribers")],
        [InlineKeyboardButton(text="📊 Bot Statistics", callback_data="admin:stats")]
    ])

def get_back_to_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Admin Panel", callback_data="admin:menu")]
    ])
