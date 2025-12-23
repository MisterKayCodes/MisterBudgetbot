from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from features.start.states.start_states import StartStates
from features.start.validators.email_validator import validate_email
from features.start.services.user_service import get_or_create_user
from database_models.users import get_user_by_telegram_id
from main_menu import get_main_menu_text, get_main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    
    if user:
        text = await get_main_menu_text(message.from_user.id)
        keyboard = await get_main_menu_keyboard(message.from_user.id)
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(
            "👋 Welcome to Mister Budget!\n\n"
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
    
    await get_or_create_user(message.from_user.id, full_name, email)
    
    await message.answer(
        f"✅ Welcome, {full_name}!\n\n"
        "Your account has been created successfully. Let's start managing your budget!"
    )
    
    await state.clear()
    
    text = await get_main_menu_text(message.from_user.id)
    keyboard = await get_main_menu_keyboard(message.from_user.id)
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery):
    text = await get_main_menu_text(callback.from_user.id)
    keyboard = await get_main_menu_keyboard(callback.from_user.id)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
