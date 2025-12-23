from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from features.admin.states.admin_states import AdminStates
from features.admin.keyboards.admin_keyboard import (
    get_admin_menu_keyboard,
    get_back_to_admin_keyboard,
    get_confirm_delete_keyboard
)
from features.admin.services.admin_service import (
    toggle_subscription_mode,
    generate_trial_code,
    get_subscribers_list,
    get_bot_statistics,
    get_all_users,
    delete_all_users
)
from utils.formatters import format_date
import config

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in config.ADMIN_IDS:
        await message.answer("⛔ Access denied. Admin only.")
        return
    
    text = "👨‍💼 Admin Panel\n\nSelect an option:"
    keyboard = get_admin_menu_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "admin:menu")
async def show_admin_menu(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    text = "👨‍💼 Admin Panel\n\nSelect an option:"
    keyboard = get_admin_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin:toggle_sub")
async def toggle_sub_mode(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    new_mode = await toggle_subscription_mode()
    
    status = "ENABLED" if new_mode == 1 else "DISABLED"
    text = f"✅ Subscription mode is now {status}"
    
    keyboard = get_back_to_admin_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer(f"Subscription mode {status.lower()}!")

@router.callback_query(F.data == "admin:trial")
async def start_trial_generation(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🎟️ Generate Trial Code\n\nEnter duration in days (e.g., 7, 30):"
    )
    await state.set_state(AdminStates.waiting_for_trial_duration)
    await callback.answer()

@router.message(AdminStates.waiting_for_trial_duration)
async def process_trial_duration(message: Message, state: FSMContext):
    if message.from_user.id not in config.ADMIN_IDS:
        await message.answer("⛔ Access denied")
        await state.clear()
        return
    
    try:
        duration = int(message.text.strip())
        
        if duration <= 0 or duration > 365:
            await message.answer("Invalid duration. Please enter a value between 1 and 365 days:")
            return
        
        code = await generate_trial_code(duration)
        
        text = f"""✅ Trial Code Generated!

Code: `{code}`
Duration: {duration} days

Share this code with users to grant them trial access."""
        
        keyboard = get_back_to_admin_keyboard()
        await message.answer(text, reply_markup=keyboard)
        
        await state.clear()
    except ValueError:
        await message.answer("Please enter a valid number:")

@router.callback_query(F.data == "admin:subscribers")
async def show_subscribers(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    subscribers = await get_subscribers_list()
    
    if not subscribers:
        text = "📋 Subscribers List\n\nNo active subscribers found."
    else:
        text = f"📋 Active Subscribers ({len(subscribers)})\n\n"
        
        for sub in subscribers[:10]:
            text += f"👤 {sub['full_name']}\n"
            text += f"   Email: {sub['email']}\n"
            text += f"   Plan: {sub['plan_type'].upper()}\n"
            text += f"   Expires: {format_date(sub['end_date']) if sub['end_date'] else 'N/A'}\n\n"
        
        if len(subscribers) > 10:
            text += f"\n... and {len(subscribers) - 10} more"
    
    keyboard = get_back_to_admin_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin:stats")
async def show_statistics(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    stats = await get_bot_statistics()
    
    text = f"""📊 Bot Statistics

👥 Total Users: {stats['total_users']}
💳 Active Subscribers: {stats['active_subscribers']}
💸 Total Transactions: {stats['total_transactions']}
🎯 Active Goals: {stats['active_goals']}"""
    
    keyboard = get_back_to_admin_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin:view_users")
async def show_all_users(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    users = await get_all_users()
    
    if not users:
        text = "👥 All Users\n\nNo users found in the database."
    else:
        text = f"👥 All Users ({len(users)})\n\n"
        
        for user in users[:15]:
            text += f"👤 {user['full_name']}\n"
            text += f"   ID: {user['telegram_id']}\n"
            text += f"   Email: {user['email']}\n"
            text += f"   Currency: {user['currency']}\n"
            text += f"   Joined: {format_date(user['created_at'])}\n\n"
        
        if len(users) > 15:
            text += f"\n... and {len(users) - 15} more users"
    
    keyboard = get_back_to_admin_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin:delete_users")
async def confirm_delete_users(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    text = """⚠️ DELETE ALL USERS

This will permanently delete:
• All user accounts
• All transactions
• All goals
• All subscriptions
• All reminders
• All accounts

This action CANNOT be undone!

Are you sure you want to continue?"""
    
    keyboard = get_confirm_delete_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "admin:confirm_delete")
async def execute_delete_users(callback: CallbackQuery):
    if callback.from_user.id not in config.ADMIN_IDS:
        await callback.answer("⛔ Access denied", show_alert=True)
        return
    
    await delete_all_users()
    
    text = "✅ All users and related data have been deleted successfully."
    
    keyboard = get_back_to_admin_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer("Database cleared!", show_alert=True)
