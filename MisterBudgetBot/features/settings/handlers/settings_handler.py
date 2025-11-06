from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from features.settings.states.settings_states import SettingsStates
from features.settings.validators.settings_validator import validate_percentage, parse_percentage
from features.settings.services.settings_service import update_user_currency, update_income_split, reset_user_data
from features.settings.keyboards.settings_keyboard import (
    get_settings_menu_keyboard,
    get_currency_keyboard,
    get_back_to_settings_keyboard,
    get_reset_confirm_keyboard
)
from database_models.users import get_user_by_telegram_id
import config

router = Router()

@router.callback_query(F.data == "menu:settings")
async def show_settings_menu(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    currency_symbols = {
        'NGN': '₦',
        'USD': '$',
        'EUR': '€'
    }
    
    text = f"""⚙️ Settings

💰 Current Currency: {user['currency']} ({currency_symbols.get(user['currency'], '')})
📊 Income Split:
  • Spending: {user['spending_percent']}%
  • Savings: {user['savings_percent']}%
  • Business: {user['business_percent']}%

Choose a setting to modify:"""
    
    keyboard = get_settings_menu_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "settings:currency")
async def show_currency_options(callback: CallbackQuery):
    text = """🌍 Change Currency

Select your preferred currency:"""
    
    keyboard = get_currency_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("settings:currency:"))
async def update_currency(callback: CallbackQuery):
    currency = callback.data.split(":")[-1]
    
    if currency not in ['NGN', 'USD', 'EUR']:
        await callback.answer("Invalid currency", show_alert=True)
        return
    
    success = await update_user_currency(callback.from_user.id, currency)
    
    if success:
        currency_names = {
            'NGN': '🇳🇬 Nigerian Naira (₦)',
            'USD': '🇺🇸 US Dollar ($)',
            'EUR': '🇪🇺 Euro (€)'
        }
        
        text = f"✅ Currency updated to {currency_names[currency]}"
        keyboard = get_back_to_settings_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
    else:
        await callback.answer("Error updating currency", show_alert=True)

@router.callback_query(F.data == "settings:split")
async def start_split_adjustment(callback: CallbackQuery, state: FSMContext):
    user = await get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("User not found")
        return
    
    await callback.message.edit_text(
        f"""📊 Adjust Income Split Percentages

Current split:
• Spending: {user['spending_percent']}%
• Savings: {user['savings_percent']}%
• Business: {user['business_percent']}%

Enter new Spending percentage (0-100):
Note: All three percentages must add up to 100%"""
    )
    
    await state.set_state(SettingsStates.waiting_for_spending_percent)
    await callback.answer()

@router.message(SettingsStates.waiting_for_spending_percent)
async def process_spending_percent(message: Message, state: FSMContext):
    if not validate_percentage(message.text):
        await message.answer("Please enter a valid percentage (0-100):")
        return
    
    spending = parse_percentage(message.text)
    await state.update_data(spending_percent=spending)
    
    await message.answer(
        f"""✅ Spending: {spending}%

Now enter Savings percentage (0-100):"""
    )
    await state.set_state(SettingsStates.waiting_for_savings_percent)

@router.message(SettingsStates.waiting_for_savings_percent)
async def process_savings_percent(message: Message, state: FSMContext):
    if not validate_percentage(message.text):
        await message.answer("Please enter a valid percentage (0-100):")
        return
    
    savings = parse_percentage(message.text)
    data = await state.get_data()
    spending = data['spending_percent']
    
    business = 100 - spending - savings
    
    if business < 0 or business > 100:
        await message.answer(
            f"""❌ Invalid split!
            
Spending: {spending}%
Savings: {savings}%
Business would be: {business}% (invalid)

The total must equal 100%. Please enter Savings percentage again:"""
        )
        return
    
    await state.update_data(savings_percent=savings, business_percent=business)
    
    await message.answer(
        f"""📊 New Split Preview:
• Spending: {spending}%
• Savings: {savings}%
• Business: {business}%

Confirm this split?""",
        reply_markup=get_back_to_settings_keyboard()
    )
    
    await state.set_state(SettingsStates.waiting_for_business_percent)

@router.message(SettingsStates.waiting_for_business_percent)
async def confirm_split_update(message: Message, state: FSMContext):
    data = await state.get_data()
    
    success = await update_income_split(
        message.from_user.id,
        data['spending_percent'],
        data['savings_percent'],
        data['business_percent']
    )
    
    if success:
        text = f"""✅ Income split updated successfully!

New split:
• Spending: {data['spending_percent']}%
• Savings: {data['savings_percent']}%
• Business: {data['business_percent']}%

This will apply to all future income."""
        
        keyboard = get_back_to_settings_keyboard()
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer("Error updating split. Please try again.")
    
    await state.clear()

@router.callback_query(F.data == "settings:reset")
async def show_reset_confirmation(callback: CallbackQuery):
    text = """⚠️ Reset All Data
    
This will permanently delete:
• All transactions (income & expenses)
• All savings goals
• All account balances (reset to 0)

Your settings (currency, split percentages) will be preserved.

Are you sure you want to continue?"""
    
    keyboard = get_reset_confirm_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "settings:reset:confirm")
async def confirm_reset_data(callback: CallbackQuery):
    success = await reset_user_data(callback.from_user.id)
    
    if success:
        text = """✅ All Data Reset Successfully!
        
Your financial data has been cleared:
✓ All transactions deleted
✓ All goals deleted
✓ All account balances reset to 0

You can start fresh with new transactions."""
        
        keyboard = get_back_to_settings_keyboard()
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer("Data reset complete!")
    else:
        await callback.answer("Error resetting data", show_alert=True)
