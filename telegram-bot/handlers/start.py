from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import StartStates
from api_client import api_client
from keyboards.main_menu import get_main_menu_keyboard
from utils.formatters import format_currency
import re

router = Router()

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await api_client.get_user(message.from_user.id)

    if user:
        balance_data = await api_client.get_total_balance(message.from_user.id)
        total_balance = balance_data.get("total_balance", 0)

        text = f"""Welcome back, {user['full_name']}!

Balance: {format_currency(total_balance, user['currency'])}

What would you like to do?"""

        await message.answer(text, reply_markup=get_main_menu_keyboard())
    else:
        await message.answer(
            "Welcome to Mister Budget!\n\n"
            "I'll help you manage your finances, track expenses, and achieve your savings goals.\n\n"
            "Let's get started! Please enter your full name:"
        )
        await state.set_state(StartStates.waiting_for_name)

@router.message(StartStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Please enter a valid name (at least 2 characters):")
        return

    await state.update_data(full_name=message.text.strip())
    await message.answer("Great! Now, please enter your email address:")
    await state.set_state(StartStates.waiting_for_email)

@router.message(StartStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    if not validate_email(message.text.strip()):
        await message.answer("Please enter a valid email address:")
        return

    data = await state.get_data()
    full_name = data.get('full_name')
    email = message.text.strip()

    try:
        await api_client.register_user(message.from_user.id, full_name, email)
        await message.answer(
            f"Welcome, {full_name}!\n\n"
            "Your account has been created successfully. Let's start managing your budget!"
        )

        await state.clear()

        await message.answer(
            "What would you like to do?",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        await message.answer(f"Error creating account: {str(e)}")
        await state.clear()

@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery):
    user = await api_client.get_user(callback.from_user.id)

    if user:
        balance_data = await api_client.get_total_balance(callback.from_user.id)
        total_balance = balance_data.get("total_balance", 0)

        text = f"""Welcome, {user['full_name']}!

Balance: {format_currency(total_balance, user['currency'])}

What would you like to do?"""

        await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard())
    await callback.answer()
