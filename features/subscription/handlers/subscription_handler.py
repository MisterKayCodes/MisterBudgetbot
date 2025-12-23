from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from features.subscription.states.subscription_states import SubscriptionStates
from features.subscription.keyboards.subscription_keyboard import (
    get_subscription_menu_keyboard,
    get_back_to_subscription_keyboard
)
from features.subscription.services.subscription_service import (
    get_user_subscription,
    redeem_trial_code,
    is_subscription_active
)
from utils.formatters import format_date
import config

router = Router()

@router.callback_query(F.data == "menu:subscription")
async def show_subscription_menu(callback: CallbackQuery):
    is_active = await is_subscription_active(callback.from_user.id)
    subscription = await get_user_subscription(callback.from_user.id)
    
    if is_active and subscription:
        text = f"""💳 Subscription Management

🟢 Status: Active
📋 Plan: {subscription['plan_type'].upper()}
📅 Start: {format_date(subscription['start_date'])}"""
        
        if subscription['end_date']:
            text += f"\n⏰ Expires: {format_date(subscription['end_date'])}"
    else:
        text = f"""💳 Subscription Management

🔴 Status: No Active Subscription

💎 Subscribe to unlock premium features!
💰 Price: {config.DEFAULT_MONTHLY_PRICE} per month

Payment: Send {config.DEFAULT_MONTHLY_PRICE} to:
{config.DEFAULT_BTC_ADDRESS}

After payment, contact admin for activation."""
    
    keyboard = get_subscription_menu_keyboard(is_active)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "subscription:status")
async def show_status(callback: CallbackQuery):
    await show_subscription_menu(callback)

@router.callback_query(F.data == "subscription:buy")
async def show_purchase_info(callback: CallbackQuery):
    text = f"""💳 Purchase Subscription

💰 Price: {config.DEFAULT_MONTHLY_PRICE} per month

Payment Instructions:
1. Send {config.DEFAULT_MONTHLY_PRICE} to:
   {config.DEFAULT_BTC_ADDRESS}

2. After payment, contact admin with:
   • Your transaction ID
   • Your Telegram username

3. Admin will activate your subscription within 24 hours.

Note: Subscriptions are manually approved by admin."""
    
    keyboard = get_back_to_subscription_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "subscription:trial")
async def start_trial_redemption(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🎟️ Redeem Trial Code\n\nEnter your trial code:"
    )
    await state.set_state(SubscriptionStates.waiting_for_trial_code)
    await callback.answer()

@router.message(SubscriptionStates.waiting_for_trial_code)
async def process_trial_code(message: Message, state: FSMContext):
    code = message.text.strip().upper()
    
    success, msg = await redeem_trial_code(message.from_user.id, code)
    
    if success:
        text = f"✅ {msg}"
        keyboard = get_back_to_subscription_keyboard()
        await message.answer(text, reply_markup=keyboard)
    else:
        text = f"❌ {msg}\n\nPlease try again or contact admin."
        keyboard = get_back_to_subscription_keyboard()
        await message.answer(text, reply_markup=keyboard)
    
    await state.clear()
