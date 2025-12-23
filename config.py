import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: List[int] = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()]

DATABASE_PATH = "data/mister_budget.db"

DEFAULT_CURRENCY = "NGN"
CURRENCY_SYMBOLS = {
    "NGN": "₦",
    "USD": "$",
    "EUR": "€"
}

DEFAULT_SPENDING_PERCENT = 60
DEFAULT_SAVINGS_PERCENT = 20
DEFAULT_BUSINESS_PERCENT = 20

DEFAULT_MONTHLY_PRICE = 10.0
DEFAULT_PRICE_3MO = 25.0
DEFAULT_PRICE_6MO = 45.0
DEFAULT_PRICE_YEAR = 80.0

DEFAULT_BTC_ADDRESS = "btc:bc1q95njz0zu39chheehws5k22j5afhk48l0ffmphw"
