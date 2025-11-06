from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from features.summary.keyboards.summary_keyboard import get_summary_menu_keyboard, get_back_to_summary_keyboard
from features.summary.services.summary_service import get_period_summary, generate_csv_export
from database_models.users import get_user_by_telegram_id
from database_models.accounts import get_total_balance
from utils.formatters import format_currency
import os

router = Router()

@router.callback_query(F.data == "menu:summary")
async def show_summary_menu(callback: CallbackQuery):
    text = """📊 Summary & Reports

View your financial summary for different time periods or export your data."""
    
    keyboard = get_summary_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "summary:weekly")
async def show_weekly_summary(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    summary = await get_period_summary(user['id'], days=7)
    total_balance = await get_total_balance(user['id'])
    currency = user['currency']
    
    text = f"""📅 Weekly Summary (Last 7 Days)

💼 Current Total Balance: {format_currency(total_balance, currency)}

📈 Income: {format_currency(summary['income_total'], currency)}
📉 Expenses: {format_currency(summary['expense_total'], currency)}
💰 Net: {format_currency(summary['net'], currency)}
📊 Transactions: {summary['transaction_count']}"""
    
    if summary['expense_by_category']:
        text += "\n\n💸 Expenses by Category:"
        for category, data in summary['expense_by_category'].items():
            text += f"\n  • {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"
    
    keyboard = get_back_to_summary_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "summary:monthly")
async def show_monthly_summary(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    summary = await get_period_summary(user['id'], days=30)
    total_balance = await get_total_balance(user['id'])
    currency = user['currency']
    
    text = f"""📆 Monthly Summary (Last 30 Days)

💼 Current Total Balance: {format_currency(total_balance, currency)}

📈 Income: {format_currency(summary['income_total'], currency)}
📉 Expenses: {format_currency(summary['expense_total'], currency)}
💰 Net: {format_currency(summary['net'], currency)}
📊 Transactions: {summary['transaction_count']}"""
    
    if summary['expense_by_category']:
        text += "\n\n💸 Expenses by Category:"
        for category, data in summary['expense_by_category'].items():
            text += f"\n  • {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"
    
    keyboard = get_back_to_summary_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "summary:alltime")
async def show_alltime_summary(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    summary = await get_period_summary(user['id'])
    total_balance = await get_total_balance(user['id'])
    currency = user['currency']
    
    text = f"""📊 All Time Statistics

💼 Current Total Balance: {format_currency(total_balance, currency)}

📈 Total Income: {format_currency(summary['income_total'], currency)}
📉 Total Expenses: {format_currency(summary['expense_total'], currency)}
💰 Net: {format_currency(summary['net'], currency)}
📊 Total Transactions: {summary['transaction_count']}"""
    
    if summary['expense_by_category']:
        text += "\n\n💸 Expenses by Category:"
        for category, data in summary['expense_by_category'].items():
            text += f"\n  • {category}: {format_currency(data['total'], currency)} ({data['count']} txns)"
    
    keyboard = get_back_to_summary_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "summary:export")
async def export_csv(callback: CallbackQuery):
    await callback.answer("Generating CSV export...")
    
    filename = await generate_csv_export(callback.from_user.id)
    
    if filename and os.path.exists(filename):
        document = FSInputFile(filename)
        await callback.message.answer_document(
            document=document,
            caption="📥 Here's your transaction history export!"
        )
        
        os.remove(filename)
        
        keyboard = get_back_to_summary_keyboard()
        await callback.message.edit_text(
            "✅ CSV export generated successfully!",
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            "❌ Error generating export. Please try again.",
            reply_markup=get_back_to_summary_keyboard()
        )
