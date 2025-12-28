from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency

router = Router()

def get_advisor_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Spending Analysis", callback_data="advisor:spending")],
        [InlineKeyboardButton(text="Savings Analysis", callback_data="advisor:saving")],
        [InlineKeyboardButton(text="Smart Recommendations", callback_data="advisor:recommendations")],
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])

@router.callback_query(F.data == "menu:advisor")
async def show_advisor_menu(callback: CallbackQuery):
    text = "Financial Advisor\n\nGet insights and recommendations about your financial habits."
    await callback.message.edit_text(text, reply_markup=get_advisor_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "advisor:spending")
async def show_spending_analysis(callback: CallbackQuery):
    try:
        analysis = await api_client.get_spending_analysis(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)
        currency = user['currency']

        text = f"""Spending Analysis (Last 30 Days)

Total Expenses: {format_currency(analysis['total_expenses'], currency)}"""

        if analysis.get('categories'):
            text += "\n\nBreakdown by Category:"
            for cat in analysis['categories'][:5]:
                text += f"\n  {cat['category']}: {format_currency(cat['total'], currency)} ({cat['percentage']:.1f}%)"

            if analysis.get('top_category'):
                text += f"\n\nTop Category: {analysis['top_category']['category']} ({analysis['top_category']['percentage']:.1f}%)"
        else:
            text += "\n\nNo expenses recorded in the last 30 days."

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "advisor:saving")
async def show_savings_analysis(callback: CallbackQuery):
    try:
        analysis = await api_client.get_savings_analysis(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)
        currency = user['currency']

        text = f"""Savings Analysis (Last 30 Days)

Savings Balance: {format_currency(analysis['savings_balance'], currency)}
Total Income: {format_currency(analysis['total_income'], currency)}
Savings Rate: {analysis['savings_rate']:.1f}%

Active Goals: {analysis['active_goals']}"""

        if analysis['active_goals'] > 0:
            goal_completion = (analysis['goal_progress'] / analysis['goal_target'] * 100) if analysis['goal_target'] > 0 else 0
            text += f"\nGoal Progress: {format_currency(analysis['goal_progress'], currency)} / {format_currency(analysis['goal_target'], currency)} ({goal_completion:.1f}%)"

        if analysis['savings_rate'] >= 20:
            text += "\n\nExcellent savings rate!"
        elif analysis['savings_rate'] >= 10:
            text += "\n\nGood savings rate. Aim for 20%!"
        else:
            text += "\n\nLow savings rate. Try to save more!"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "advisor:recommendations")
async def show_recommendations(callback: CallbackQuery):
    try:
        result = await api_client.get_recommendations(callback.from_user.id)
        recommendations = result.get('recommendations', [])

        text = "Smart Recommendations\n\n"
        text += "\n\n".join(recommendations)

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()
