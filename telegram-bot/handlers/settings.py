from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.states import SettingsStates
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard

router = Router()

def get_settings_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Change Currency", callback_data="settings:currency")],
        [InlineKeyboardButton(text="Adjust Split %", callback_data="settings:split")],
        [InlineKeyboardButton(text="Back to Main Menu", callback_data="menu:main")]
    ])

def get_currency_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="NGN", callback_data="settings:currency:NGN"),
            InlineKeyboardButton(text="USD", callback_data="settings:currency:USD")
        ],
        [InlineKeyboardButton(text="EUR", callback_data="settings:currency:EUR")],
        [InlineKeyboardButton(text="Back", callback_data="menu:settings")]
    ])

@router.callback_query(F.data == "menu:settings")
async def show_settings_menu(callback: CallbackQuery):
    user = await api_client.get_user(callback.from_user.id)

    if user:
        text = f"""Settings

Current Currency: {user['currency']}
Income Split:
  Spending: {user['spending_percent']}%
  Savings: {user['savings_percent']}%
  Business: {user['business_percent']}%

Choose a setting to modify:"""

        await callback.message.edit_text(text, reply_markup=get_settings_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "settings:currency")
async def show_currency_options(callback: CallbackQuery):
    text = "Change Currency\n\nSelect your preferred currency:"
    await callback.message.edit_text(text, reply_markup=get_currency_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("settings:currency:"))
async def update_currency(callback: CallbackQuery):
    currency = callback.data.split(":")[-1]

    try:
        await api_client.update_user(callback.from_user.id, {"currency": currency})

        currency_names = {
            'NGN': 'Nigerian Naira',
            'USD': 'US Dollar',
            'EUR': 'Euro'
        }

        text = f"Currency updated to {currency_names[currency]}"
        await callback.message.edit_text(text, reply_markup=get_back_to_main_keyboard())
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(
            f"Error: {str(e)}",
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer()

@router.callback_query(F.data == "settings:split")
async def start_split_adjustment(callback: CallbackQuery, state: FSMContext):
    user = await api_client.get_user(callback.from_user.id)

    if user:
        await callback.message.edit_text(
            f"""Adjust Income Split Percentages

Current split:
Spending: {user['spending_percent']}%
Savings: {user['savings_percent']}%
Business: {user['business_percent']}%

Enter new Spending percentage (0-100):
Note: All three percentages must add up to 100%"""
        )

        await state.set_state(SettingsStates.waiting_for_spending_percent)
        await callback.answer()

@router.message(SettingsStates.waiting_for_spending_percent)
async def process_spending_percent(message: Message, state: FSMContext):
    try:
        spending = int(message.text.strip())
        if spending < 0 or spending > 100:
            raise ValueError

        await state.update_data(spending_percent=spending)
        await message.answer(f"Spending: {spending}%\n\nNow enter Savings percentage (0-100):")
        await state.set_state(SettingsStates.waiting_for_savings_percent)

    except ValueError:
        await message.answer("Please enter a valid percentage (0-100):")

@router.message(SettingsStates.waiting_for_savings_percent)
async def process_savings_percent(message: Message, state: FSMContext):
    try:
        savings = int(message.text.strip())
        if savings < 0 or savings > 100:
            raise ValueError

        data = await state.get_data()
        spending = data['spending_percent']
        business = 100 - spending - savings

        if business < 0 or business > 100:
            await message.answer(
                f"Invalid split!\n\n"
                f"Spending: {spending}%\n"
                f"Savings: {savings}%\n"
                f"Business would be: {business}% (invalid)\n\n"
                "The total must equal 100%. Please enter Savings percentage again:"
            )
            return

        await api_client.update_user(message.from_user.id, {
            "spending_percent": spending,
            "savings_percent": savings,
            "business_percent": business
        })

        text = f"""Income split updated successfully!

New split:
Spending: {spending}%
Savings: {savings}%
Business: {business}%

This will apply to all future income."""

        await message.answer(text, reply_markup=get_back_to_main_keyboard())
        await state.clear()

    except ValueError:
        await message.answer("Please enter a valid percentage (0-100):")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
        await state.clear()
