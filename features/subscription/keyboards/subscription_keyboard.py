from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

def get_subscription_menu_keyboard(is_active: bool) -> InlineKeyboardMarkup:
    buttons = []
    
    if is_active:
        buttons.append([InlineKeyboardButton(text="🟢 Active Subscription", callback_data="subscription:status")])
    else:
        buttons.append([InlineKeyboardButton(text="🔴 No Active Subscription", callback_data="subscription:status")])
        buttons.append([InlineKeyboardButton(text="💳 Subscribe Now", callback_data="subscription:buy")])
        buttons.append([InlineKeyboardButton(text="🎟️ Redeem Trial Code", callback_data="subscription:trial")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_to_subscription_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Subscription", callback_data="menu:subscription")]
    ])
