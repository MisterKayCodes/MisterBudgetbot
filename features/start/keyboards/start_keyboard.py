from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_welcome_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Get Started", callback_data="start:begin")]
    ])
