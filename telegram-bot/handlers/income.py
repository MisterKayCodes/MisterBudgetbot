from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.states import IncomeStates
from api_client import api_client
from keyboards.main_menu import get_back_to_main_keyboard
from utils.formatters import format_currency

router = Router()

@router.callback_query(F.data == "menu:add_income")
async def start_add_income(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Enter the income amount:\n\n"
        "Example: 50000 or 50,000"
    )
    await state.set_state(IncomeStates.waiting_for_amount)
    await callback.answer()

@router.message(IncomeStates.waiting_for_amount)
async def process_income_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", ""))
        if amount <= 0:
            raise ValueError

        result = await api_client.add_income(message.from_user.id, amount)
        user = await api_client.get_user(message.from_user.id)

        splits = result['splits']

        text = f"""Income: {format_currency(amount, user['currency'])} received!

Split breakdown:
 {format_currency(splits['spending'], user['currency'])} - Spending
 {format_currency(splits['savings'], user['currency'])} - Savings
 {format_currency(splits['business'], user['currency'])} - Business"""

        if result.get('goal_allocations'):
            text += "\n\nGoal allocations:"
            for ga in result['goal_allocations']:
                text += f"\n {format_currency(ga['amount'], user['currency'])} - {ga['goal_name']} ({ga['percent']}%)"

        await message.answer(text, reply_markup=get_back_to_main_keyboard())
        await state.clear()

    except ValueError:
        await message.answer("Please enter a valid amount (positive number):")
    except Exception as e:
        await message.answer(f"Error processing income: {str(e)}")
        await state.clear()
