from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.states import ExpenseStates
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency

router = Router()

def get_category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Food", callback_data="expense:cat:Food"),
            InlineKeyboardButton(text="Transport", callback_data="expense:cat:Transport")
        ],
        [
            InlineKeyboardButton(text="Housing", callback_data="expense:cat:Housing"),
            InlineKeyboardButton(text="Entertainment", callback_data="expense:cat:Entertainment")
        ],
        [
            InlineKeyboardButton(text="Shopping", callback_data="expense:cat:Shopping"),
            InlineKeyboardButton(text="Health", callback_data="expense:cat:Health")
        ],
        [InlineKeyboardButton(text="Skip Category", callback_data="expense:cat:General")]
    ])

@router.callback_query(F.data == "menu:add_expense")
async def start_add_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Enter the expense name/description:\n\n"
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
    await message.answer("Now enter the amount:")
    await state.set_state(ExpenseStates.waiting_for_amount)

@router.message(ExpenseStates.waiting_for_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", ""))
        if amount <= 0:
            raise ValueError

        await state.update_data(expense_amount=amount)
        await message.answer(
            "Select a category:",
            reply_markup=get_category_keyboard()
        )
    except ValueError:
        await message.answer("Please enter a valid amount (positive number):")

@router.callback_query(F.data.startswith("expense:cat:"))
async def process_expense_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[-1]
    data = await state.get_data()

    name = data.get('expense_name')
    amount = data.get('expense_amount')

    try:
        result = await api_client.add_expense(
            callback.from_user.id,
            name,
            amount,
            category
        )

        user = await api_client.get_user(callback.from_user.id)

        text = f"""Expense logged successfully!

{name}
{format_currency(amount, user['currency'])}
Category: {category}

Deducted from your Spending Account."""

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await state.clear()
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await state.clear()
        await callback.answer()
