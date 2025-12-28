from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.states import GoalsStates
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency, calculate_progress_bar, format_percentage

router = Router()

def get_goals_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Create New Goal", callback_data="goals:create")],
        [InlineKeyboardButton(text="View Active Goals", callback_data="goals:active")],
        [InlineKeyboardButton(text="Completed Goals", callback_data="goals:completed")],
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])

@router.callback_query(F.data == "menu:goals")
async def show_goals_menu(callback: CallbackQuery):
    text = "Goals Management\n\nChoose an option:"
    await callback.message.edit_text(text, reply_markup=get_goals_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "goals:create")
async def start_create_goal(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Create a New Goal\n\n"
        "Enter the goal name:\n"
        "Example: Buy New Phone"
    )
    await state.set_state(GoalsStates.waiting_for_goal_name)
    await callback.answer()

@router.message(GoalsStates.waiting_for_goal_name)
async def process_goal_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Please enter a valid goal name (at least 2 characters):")
        return

    await state.update_data(goal_name=message.text.strip())
    await message.answer("Enter the target amount:")
    await state.set_state(GoalsStates.waiting_for_target_amount)

@router.message(GoalsStates.waiting_for_target_amount)
async def process_target_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", ""))
        if amount <= 0:
            raise ValueError
    except:
        await message.answer("Please enter a valid amount (positive number):")
        return

    await state.update_data(target_amount=amount)

    skip_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Skip Auto-Save", callback_data="goals:skip_autosave")]
    ])

    await message.answer(
        "Set auto-save percentage (0-100):\n\n"
        "This percentage will be automatically saved from each income.\n"
        "Or skip if you don't want auto-save.",
        reply_markup=skip_kb
    )
    await state.set_state(GoalsStates.waiting_for_auto_save_percent)

@router.callback_query(F.data == "goals:skip_autosave")
async def skip_autosave(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    try:
        result = await api_client.create_goal(
            callback.from_user.id,
            data['goal_name'],
            data['target_amount'],
            None,
            0
        )

        user = await api_client.get_user(callback.from_user.id)

        text = f"""Goal created successfully!

{data['goal_name']}
Target: {format_currency(data['target_amount'], user['currency'])}"""

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await state.clear()
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error creating goal: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await state.clear()
        await callback.answer()

@router.message(GoalsStates.waiting_for_auto_save_percent)
async def process_auto_save(message: Message, state: FSMContext):
    try:
        percent = int(message.text)
        if percent < 0 or percent > 100:
            raise ValueError
    except:
        await message.answer("Please enter a valid percentage (0-100):")
        return

    data = await state.get_data()

    try:
        result = await api_client.create_goal(
            message.from_user.id,
            data['goal_name'],
            data['target_amount'],
            None,
            percent
        )

        user = await api_client.get_user(message.from_user.id)

        text = f"""Goal created successfully!

{data['goal_name']}
Target: {format_currency(data['target_amount'], user['currency'])}
Auto-save: {percent}% of each income"""

        await message.answer(text, reply_markup=get_back_to_main_keyboard())
        await state.clear()

    except Exception as e:
        await message.answer(f"Error creating goal: {str(e)}")
        await state.clear()

@router.callback_query(F.data == "goals:active")
async def show_active_goals(callback: CallbackQuery):
    try:
        goals = await api_client.get_active_goals(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)

        if not goals:
            text = "No active goals found.\n\nCreate a new goal to get started!"
        else:
            text = "Active Goals:\n\n"
            for goal in goals:
                progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
                bar = calculate_progress_bar(goal['current_amount'], goal['target_amount'])

                text += f"{goal['goal_name']}\n"
                text += f"{bar} {format_percentage(progress)}\n"
                text += f"{format_currency(goal['current_amount'], user['currency'])} / {format_currency(goal['target_amount'], user['currency'])}\n\n"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "goals:completed")
async def show_completed_goals(callback: CallbackQuery):
    try:
        goals = await api_client.get_completed_goals(callback.from_user.id)
        user = await api_client.get_user(callback.from_user.id)

        if not goals:
            text = "No completed goals yet.\n\nKeep working towards your active goals!"
        else:
            text = "Completed Goals:\n\n"
            for goal in goals:
                text += f"{goal['goal_name']}\n"
                text += f"{format_currency(goal['current_amount'], user['currency'])}\n\n"

        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()
