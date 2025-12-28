from datetime import datetime
from typing import Optional
from config import CURRENCY_SYMBOLS

def format_currency(amount: float, currency: str = "NGN") -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def format_date(date_str: Optional[str] = None) -> str:
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_str
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def calculate_progress_bar(current: float, target: float, length: int = 10) -> str:
    if target <= 0:
        return "▱" * length

    progress = min(current / target, 1.0)
    filled = int(progress * length)
    return "▰" * filled + "▱" * (length - filled)

def format_percentage(value: float) -> str:
    return f"{value:.1f}%"
