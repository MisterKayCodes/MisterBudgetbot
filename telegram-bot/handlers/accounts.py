from aiogram import Router, F
from aiogram.types import CallbackQuery
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency

router = Router()

@router.callback_query(F.data == "menu:accounts")
async def show_accounts(callback: CallbackQuery):
    try:
        user = await api_client.get_user(callback.from_user.id)
        accounts = await api_client.get_accounts(callback.from_user.id)

        text = "Your Accounts:\n\n"

        for account in accounts:
            if account['account_type'] != 'main':
                icon = {
                    "spending": "Spending",
                    "savings": "Savings",
                    "business": "Business"
                }.get(account['account_type'], "Account")

                text += f"{icon}: {format_currency(account['balance'], user['currency'])}\n"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()
