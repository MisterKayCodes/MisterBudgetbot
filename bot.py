import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import init_database
from utils.logger import logger

from features.start.handlers import start_handler
from features.income.handlers import income_handler
from features.expense.handlers import expense_handler
from features.goals.handlers import goals_handler
from features.summary.handlers import summary_handler
from features.advisor.handlers import advisor_handler
from features.settings.handlers import settings_handler
from features.accounts.handlers import accounts_handler
from features.reminders.handlers import reminders_handler
from features.subscription.handlers import subscription_handler
from features.admin.handlers import admin_handler


async def main():
    logger.info("🚀 Starting Mister Budget bot...")

    # Initialize database
    await init_database()
    logger.info("✅ Database initialized successfully")

    # Setup bot and dispatcher
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Include feature routers
    dp.include_router(start_handler.router)
    dp.include_router(income_handler.router)
    dp.include_router(expense_handler.router)
    dp.include_router(goals_handler.router)
    dp.include_router(summary_handler.router)
    dp.include_router(advisor_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(accounts_handler.router)
    dp.include_router(reminders_handler.router)
    dp.include_router(subscription_handler.router)
    dp.include_router(admin_handler.router)

    logger.info("🔌 All routers registered")

    # Ensure old updates are dropped
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("🤖 Bot is now polling for updates...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("🛑 Stopping bot gracefully...")
        await bot.session.close()
        logger.info("✅ Bot shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped manually by user (Ctrl + C).")
    except Exception as e:
        logger.error(f"🔥 Bot crashed: {e}")
