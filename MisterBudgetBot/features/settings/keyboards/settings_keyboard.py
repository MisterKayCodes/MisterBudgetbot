from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_settings_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Change Currency", callback_data="settings:currency")],
        [InlineKeyboardButton(text="📊 Adjust Split %", callback_data="settings:split")],
        [InlineKeyboardButton(text="🗑️ Reset All Data", callback_data="settings:reset")],
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])

def get_reset_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yes, Reset Everything", callback_data="settings:reset:confirm")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="menu:settings")]
    ])

def get_currency_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇳🇬 NGN (₦)", callback_data="settings:currency:NGN"),
            InlineKeyboardButton(text="🇺🇸 USD ($)", callback_data="settings:currency:USD")
        ],
        [
            InlineKeyboardButton(text="🇪🇺 EUR (€)", callback_data="settings:currency:EUR")
        ],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="menu:settings")]
    ])

def get_back_to_settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Settings", callback_data="menu:settings")]
    ])
