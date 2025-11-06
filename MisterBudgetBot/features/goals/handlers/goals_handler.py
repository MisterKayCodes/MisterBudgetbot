from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from features.goals.states.goals_states import GoalsStates
from features.goals.keyboards.goals_keyboard import (
    get_goals_menu_keyboard,
    get_skip_deadline_keyboard,
    get_back_to_goals_keyboard
)
from features.goals.services.goals_service import add_new_goal
from database_models.goals import get_active_goals, get_completed_goals
from database_models.users import get_user_by_telegram_id
from utils.formatters import format_currency, calculate_progress_bar, format_percentage

router = Router()

@router.callback_query(F.data == "menu:goals")
async def show_goals_menu(callback: CallbackQuery):
    text = "🎯 Goals Management\n\nChoose an option:"
    keyboard = get_goals_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "goals:create")
async def start_create_goal(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎯 Create a New Goal\n\n"
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
    await message.answer("💰 Enter the target amount:")
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
    
    keyboard = get_skip_deadline_keyboard()
    await message.answer(
        "📅 Enter a deadline (YYYY-MM-DD) or skip:",
        reply_markup=keyboard
    )
    await state.set_state(GoalsStates.waiting_for_deadline)

@router.callback_query(F.data == "goals:skip_deadline", GoalsStates.waiting_for_deadline)
async def skip_deadline(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "💡 Set auto-save percentage (0-100):\n\n"
        "This percentage will be automatically saved from each income.\n"
        "Enter 0 to skip auto-save."
    )
    await state.set_state(GoalsStates.waiting_for_auto_save_percent)
    await callback.answer()

@router.message(GoalsStates.waiting_for_deadline)
async def process_deadline(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text.strip())
    await message.answer(
        "💡 Set auto-save percentage (0-100):\n\n"
        "This percentage will be automatically saved from each income.\n"
        "Enter 0 to skip auto-save."
    )
    await state.set_state(GoalsStates.waiting_for_auto_save_percent)

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
    
    success = await add_new_goal(
        message.from_user.id,
        data['goal_name'],
        data['target_amount'],
        data.get('deadline'),
        percent
    )
    
    if success:
        user = await get_user_by_telegram_id(message.from_user.id)
        text = f"""✅ Goal created successfully!

🎯 {data['goal_name']}
💰 Target: {format_currency(data['target_amount'], user['currency'])}"""
        
        if data.get('deadline'):
            text += f"\n📅 Deadline: {data['deadline']}"
        if percent > 0:
            text += f"\n💡 Auto-save: {percent}% of each income"
    else:
        text = "❌ Error creating goal. Please try again."
    
    keyboard = get_back_to_goals_keyboard()
    await message.answer(text, reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == "goals:active")
async def show_active_goals(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    goals = await get_active_goals(user['id'])
    
    if not goals:
        text = "📈 No active goals found.\n\nCreate a new goal to get started!"
    else:
        text = "📈 Active Goals:\n\n"
        for goal in goals:
            progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
            bar = calculate_progress_bar(goal['current_amount'], goal['target_amount'])
            
            text += f"🎯 {goal['goal_name']}\n"
            text += f"{bar} {format_percentage(progress)}\n"
            text += f"{format_currency(goal['current_amount'], user['currency'])} / {format_currency(goal['target_amount'], user['currency'])}\n"
            if goal['deadline']:
                text += f"📅 Deadline: {goal['deadline']}\n"
            text += "\n"
    
    keyboard = get_back_to_goals_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "goals:completed")
async def show_completed_goals(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    goals = await get_completed_goals(user['id'])
    
    if not goals:
        text = "✅ No completed goals yet.\n\nKeep working towards your active goals!"
    else:
        text = "✅ Completed Goals:\n\n"
        for goal in goals:
            text += f"🎯 {goal['goal_name']}\n"
            text += f"💰 {format_currency(goal['current_amount'], user['currency'])}\n\n"
    
    keyboard = get_back_to_goals_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
