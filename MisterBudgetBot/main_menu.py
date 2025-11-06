from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database_models.users import get_user_by_telegram_id
from database_models.accounts import get_total_balance, get_account_by_type
from database_models.transactions import get_monthly_expenses
from database_models.goals import get_active_goals
from utils.formatters import format_currency
import config

async def get_main_menu_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    user = await get_user_by_telegram_id(telegram_id)
    
    db = await __import__('database').get_db()
    cursor = await db.execute("SELECT subscription_mode FROM admin_settings WHERE id = 1")
    settings = await cursor.fetchone()
    await db.close()
    
    subscription_enabled = settings and settings['subscription_mode'] == 1
    
    buttons = [
        [
            InlineKeyboardButton(text="➕ Add Income", callback_data="menu:add_income"),
            InlineKeyboardButton(text="➖ Add Expense", callback_data="menu:add_expense")
        ],
        [
            InlineKeyboardButton(text="🎯 My Goals", callback_data="menu:goals"),
            InlineKeyboardButton(text="🧠 Advisor", callback_data="menu:advisor")
        ],
        [
            InlineKeyboardButton(text="📊 Summary", callback_data="menu:summary"),
            InlineKeyboardButton(text="⚙️ Settings", callback_data="menu:settings")
        ],
        [
            InlineKeyboardButton(text="💼 Accounts", callback_data="menu:accounts"),
            InlineKeyboardButton(text="🗓️ Reminders", callback_data="menu:reminders")
        ]
    ]
    
    if subscription_enabled:
        buttons.append([
            InlineKeyboardButton(text="💳 Subscription", callback_data="menu:subscription")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_main_menu_text(telegram_id: int) -> str:
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return "User not found. Please /start again."
    
    total_balance = await get_total_balance(user['id'])
    monthly_expenses = await get_monthly_expenses(user['id'])
    active_goals = await get_active_goals(user['id'])
    
    savings_account = await get_account_by_type(user['id'], 'savings')
    total_savings = savings_account['balance'] if savings_account else 0.0
    
    currency = user['currency']
    
    text = f"""👋 Hi, {user['full_name']}!

💼 Main Balance: {format_currency(total_balance, currency)}
💸 Expenses (This Month): {format_currency(monthly_expenses, currency)}
💰 Savings: {format_currency(total_savings, currency)}
🎯 Active Goals: {len(active_goals)}

What would you like to do today?"""
    
    return text
