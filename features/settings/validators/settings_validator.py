def validate_percentage(text: str) -> bool:
    try:
        value = int(text.strip())
        return 0 <= value <= 100
    except ValueError:
        return False

def parse_percentage(text: str) -> int:
    return int(text.strip())
