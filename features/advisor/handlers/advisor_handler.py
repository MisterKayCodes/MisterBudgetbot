from aiogram import Router, F
from aiogram.types import CallbackQuery
from features.advisor.keyboards.advisor_keyboard import get_advisor_menu_keyboard, get_back_to_advisor_keyboard
from features.advisor.services.advisor_service import (
    analyze_spending_habits,
    analyze_savings_habits,
    generate_recommendations
)
from database_models.users import get_user_by_telegram_id
from utils.formatters import format_currency

router = Router()

@router.callback_query(F.data == "menu:advisor")
async def show_advisor_menu(callback: CallbackQuery):
    text = """🧠 Financial Advisor

Get insights and recommendations about your financial habits."""
    
    keyboard = get_advisor_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "advisor:spending")
async def show_spending_analysis(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    analysis = await analyze_spending_habits(user['id'])
    currency = user['currency']
    
    text = f"""📈 Spending Analysis (Last 30 Days)

💸 Total Expenses: {format_currency(analysis['total_expenses'], currency)}"""
    
    if analysis['categories']:
        text += "\n\n💳 Breakdown by Category:"
        for cat in analysis['categories'][:5]:
            text += f"\n  • {cat['category']}: {format_currency(cat['total'], currency)} ({cat['percentage']:.1f}%)"
        
        if analysis['top_category']:
            text += f"\n\n🔝 Top Category: {analysis['top_category']['category']} ({analysis['top_category']['percentage']:.1f}%)"
    else:
        text += "\n\nNo expenses recorded in the last 30 days."
    
    keyboard = get_back_to_advisor_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "advisor:saving")
async def show_savings_analysis(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    analysis = await analyze_savings_habits(user['id'])
    currency = user['currency']
    
    text = f"""💰 Savings Analysis (Last 30 Days)

💼 Savings Balance: {format_currency(analysis['savings_balance'], currency)}
📈 Total Income: {format_currency(analysis['total_income'], currency)}
📊 Savings Rate: {analysis['savings_rate']:.1f}%

🎯 Active Goals: {analysis['active_goals']}"""
    
    if analysis['active_goals'] > 0:
        goal_completion = (analysis['goal_progress'] / analysis['goal_target'] * 100) if analysis['goal_target'] > 0 else 0
        text += f"\n💪 Goal Progress: {format_currency(analysis['goal_progress'], currency)} / {format_currency(analysis['goal_target'], currency)} ({goal_completion:.1f}%)"
    
    if analysis['savings_rate'] >= 20:
        text += "\n\n🟢 Excellent savings rate!"
    elif analysis['savings_rate'] >= 10:
        text += "\n\n🟡 Good savings rate. Aim for 20%!"
    else:
        text += "\n\n🔴 Low savings rate. Try to save more!"
    
    keyboard = get_back_to_advisor_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "advisor:recommendations")
async def show_recommendations(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    recommendations = await generate_recommendations(user['id'])
    
    text = "💡 Smart Recommendations\n\n"
    text += "\n\n".join(recommendations)
    
    keyboard = get_back_to_advisor_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
