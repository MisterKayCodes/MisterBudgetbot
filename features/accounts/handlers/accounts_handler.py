from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database_models.users import get_user_by_telegram_id
from database_models.accounts import get_user_accounts
from utils.formatters import format_currency

router = Router()

@router.callback_query(F.data == "menu:accounts")
async def show_accounts_menu(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    accounts = await get_user_accounts(user['id'])
    
    text = "💼 Your Accounts:\n\n"
    
    for account in accounts:
        if account['account_type'] != 'main':
            icon = {"spending": "💸", "savings": "💰", "business": "🏗️"}.get(account['account_type'], "📊")
            text += f"{icon} {account['account_name']}: {format_currency(account['balance'], user['currency'])}\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="menu:main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
