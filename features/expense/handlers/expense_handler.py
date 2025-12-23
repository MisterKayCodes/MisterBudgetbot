from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from features.expense.states.expense_states import ExpenseStates
from features.expense.validators.expense_validator import validate_amount, parse_amount
from features.expense.services.expense_service import process_expense
from features.expense.keyboards.expense_keyboard import (
    get_expense_menu_keyboard,
    get_category_keyboard,
    get_back_to_expense_keyboard
)
from database_models.transactions import get_recent_transactions
from database_models.users import get_user_by_telegram_id
from utils.formatters import format_currency, format_date

router = Router()

@router.callback_query(F.data == "menu:add_expense")
async def show_expense_menu(callback: CallbackQuery):
    text = "💸 Expense Management\n\nChoose an option:"
    keyboard = get_expense_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "expense:add")
async def start_add_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 Enter the expense name/description:\n\n"
        "Example: Lunch at restaurant"
    )
    await state.set_state(ExpenseStates.waiting_for_name)
    await callback.answer()

@router.message(ExpenseStates.waiting_for_name)
async def process_expense_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Please enter a valid description (at least 2 characters):")
        return
    
    await state.update_data(expense_name=message.text.strip())
    await message.answer("💰 Now enter the amount:")
    await state.set_state(ExpenseStates.waiting_for_amount)

@router.message(ExpenseStates.waiting_for_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    if not validate_amount(message.text):
        await message.answer("Please enter a valid amount (positive number):")
        return
    
    amount = parse_amount(message.text)
    await state.update_data(expense_amount=amount)
    
    keyboard = get_category_keyboard()
    await message.answer(
        "🏷️ Select a category (optional):",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("expense:cat:"))
async def process_expense_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[-1]
    data = await state.get_data()
    
    name = data.get('expense_name')
    amount = data.get('expense_amount')
    
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    success, message_text = await process_expense(
        callback.from_user.id,
        name,
        amount,
        category
    )
    
    if success:
        text = f"""✅ Expense logged successfully!

📝 {name}
💰 {format_currency(amount, user['currency'])}
🏷️ Category: {category}

Deducted from your Spending Account."""
    else:
        text = f"❌ Error: {message_text}"
    
    keyboard = get_back_to_expense_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "expense:recent")
async def show_recent_expenses(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    transactions = await get_recent_transactions(user['id'], 'expense', 10)
    
    if not transactions:
        text = "📂 No recent expense records found."
    else:
        text = "📂 Recent Expenses:\n\n"
        for txn in transactions:
            text += f"💸 {txn['description'] or 'Expense'}\n"
            text += f"   {format_currency(txn['amount'], user['currency'])}"
            if txn['category']:
                text += f" - {txn['category']}"
            text += f"\n   {format_date(txn['created_at'])}\n\n"
    
    keyboard = get_back_to_expense_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
