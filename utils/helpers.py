from typing import Optional
import re
from datetime import datetime

def get_current_datetime() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_amount(text: str) -> bool:
    try:
        amount = float(text.replace(",", ""))
        return amount > 0
    except:
        return False

def parse_amount(text: str) -> Optional[float]:
    try:
        return float(text.replace(",", ""))
    except:
        return None

def split_income(amount: float, spending_pct: int, savings_pct: int, business_pct: int) -> dict:
    return {
        "spending": round(amount * spending_pct / 100, 2),
        "savings": round(amount * savings_pct / 100, 2),
        "business": round(amount * business_pct / 100, 2)
    }
