def validate_amount(text: str) -> bool:
    try:
        amount = float(text.replace(",", ""))
        return amount > 0
    except:
        return False

def parse_amount(text: str) -> float:
    try:
        return float(text.replace(",", ""))
    except:
        return 0.0
