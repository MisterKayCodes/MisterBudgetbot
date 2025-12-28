from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency

router = Router()

def get_summary_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Weekly Report", callback_data="summary:weekly")],
        [InlineKeyboardButton(text="Monthly Report", callback_data="summary:monthly")],
        [InlineKeyboardButton(text="All Time Stats", callback_data="summary:alltime")],
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])

@router.callback_query(F.data == "menu:summary")
async def show_summary_menu(callback: CallbackQuery):
    text = "Summary & Reports\n\nView your financial summary for different time periods."
    await callback.message.edit_text(text, reply_markup=get_summary_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "summary:weekly")
async def show_weekly_summary(callback: CallbackQuery):
    try:
        summary = await api_client.get_weekly_summary(callback.from_user.id)
        balance_data = await api_client.get_total_balance(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)

        currency = user['currency']
        total_balance = balance_data.get("total_balance", 0)

        text = f"""Weekly Summary (Last 7 Days)

Current Total Balance: {format_currency(total_balance, currency)}

Income: {format_currency(summary['income_total'], currency)}
Expenses: {format_currency(summary['expense_total'], currency)}
Net: {format_currency(summary['net'], currency)}
Transactions: {summary['transaction_count']}"""

        if summary.get('expense_by_category'):
            text += "\n\nExpenses by Category:"
            for category, data in summary['expense_by_category'].items():
                text += f"\n  {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "summary:monthly")
async def show_monthly_summary(callback: CallbackQuery):
    try:
        summary = await api_client.get_monthly_summary(callback.from_user.id)
        balance_data = await api_client.get_total_balance(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)

        currency = user['currency']
        total_balance = balance_data.get("total_balance", 0)

        text = f"""Monthly Summary (Last 30 Days)

Current Total Balance: {format_currency(total_balance, currency)}

Income: {format_currency(summary['income_total'], currency)}
Expenses: {format_currency(summary['expense_total'], currency)}
Net: {format_currency(summary['net'], currency)}
Transactions: {summary['transaction_count']}"""

        if summary.get('expense_by_category'):
            text += "\n\nExpenses by Category:"
            for category, data in summary['expense_by_category'].items():
                text += f"\n  {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "summary:alltime")
async def show_alltime_summary(callback: CallbackQuery):
    try:
        summary = await api_client.get_alltime_summary(callback.from_user.id)
        balance_data = await api_client.get_total_balance(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)

        currency = user['currency']
        total_balance = balance_data.get("total_balance", 0)

        text = f"""All Time Statistics

Current Total Balance: {format_currency(total_balance, currency)}

Total Income: {format_currency(summary['income_total'], currency)}
Total Expenses: {format_currency(summary['expense_total'], currency)}
Net: {format_currency(summary['net'], currency)}
Total Transactions: {summary['transaction_count']}"""

        if summary.get('expense_by_category'):
            text += "\n\nExpenses by Category:"
            for category, data in summary['expense_by_category'].items():
                text += f"\n  {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()
