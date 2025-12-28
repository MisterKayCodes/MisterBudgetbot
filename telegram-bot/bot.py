import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from api_client import api_client
from handlers import start, income, expense, goals, summary, advisor, settings, accounts, reminders

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting Mister Budget bot...")

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(income.router)
    dp.include_router(expense.router)
    dp.include_router(goals.router)
    dp.include_router(summary.router)
    dp.include_router(advisor.router)
    dp.include_router(settings.router)
    dp.include_router(accounts.router)
    dp.include_router(reminders.router)

    logger.info("All routers registered")

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Bot is now polling for updates...")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Stopping bot gracefully...")
        await api_client.close()
        await bot.session.close()
        logger.info("Bot shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually by user.")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
