from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from features.income.states.income_states import IncomeStates
from features.income.validators.income_validator import validate_amount, parse_amount
from features.income.services.income_service import process_income
from features.income.keyboards.income_keyboard import get_income_menu_keyboard, get_back_to_income_keyboard
from database_models.transactions import get_recent_transactions
from database_models.users import get_user_by_telegram_id
from database_models.goals import get_active_goals
from utils.formatters import format_currency, format_date

router = Router()

@router.callback_query(F.data == "menu:add_income")
async def show_income_menu(callback: CallbackQuery):
    text = "💵 Income Management\n\nChoose an option:"
    keyboard = get_income_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "income:add")
async def start_add_income(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "💰 Enter the income amount:\n\n"
        "Example: 50000 or 50,000"
    )
    await state.set_state(IncomeStates.waiting_for_amount)
    await callback.answer()

@router.message(IncomeStates.waiting_for_amount)
async def process_income_amount(message: Message, state: FSMContext):
    if not validate_amount(message.text):
        await message.answer("Please enter a valid amount (positive number):")
        return
    
    amount = parse_amount(message.text)
    user = await get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("User not found. Please /start again.")
        await state.clear()
        return
    
    splits = await process_income(message.from_user.id, amount)
    
    if splits:
        currency = user['currency']
        text = f"""✅ Income: {format_currency(amount, currency)} received!

💸 Split breakdown:
➤ {format_currency(splits['spending'], currency)} → Spending ({user['spending_percent']}%)
➤ {format_currency(splits['savings'], currency)} → Savings ({user['savings_percent']}%)
➤ {format_currency(splits['business'], currency)} → Business ({user['business_percent']}%)"""
        
        active_goals = await get_active_goals(user['id'])
        goals_with_auto_save = [g for g in active_goals if g['auto_save_percent'] > 0]
        
        if goals_with_auto_save:
            text += "\n\n🎯 Goal allocations:"
            for goal in goals_with_auto_save:
                goal_amount = amount * goal['auto_save_percent'] / 100
                text += f"\n➤ {format_currency(goal_amount, currency)} → {goal['goal_name']} ({goal['auto_save_percent']}%)"
        
        text += "\n\nYour accounts have been updated."
        
        keyboard = get_back_to_income_keyboard()
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer("Error processing income. Please try again.")
    
    await state.clear()

@router.callback_query(F.data == "income:recent")
async def show_recent_incomes(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    transactions = await get_recent_transactions(user['id'], 'income', 10)
    
    if not transactions:
        text = "📂 No recent income records found."
    else:
        text = "📂 Recent Incomes:\n\n"
        for txn in transactions:
            text += f"💰 {format_currency(txn['amount'], user['currency'])}\n"
            text += f"   {format_date(txn['created_at'])}\n"
            if txn['description']:
                text += f"   {txn['description']}\n"
            text += "\n"
    
    keyboard = get_back_to_income_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
