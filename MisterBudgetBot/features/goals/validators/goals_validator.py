def validate_amount(text: str) -> bool:
    try:
        amount = float(text.replace(",", ""))
        return amount > 0
    except:
        return False
