from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    supabase_service_key: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080

    admin_ids: str = ""

    default_currency: str = "NGN"
    default_spending_percent: int = 60
    default_savings_percent: int = 20
    default_business_percent: int = 20

    default_monthly_price: float = 10.0
    default_price_3mo: float = 25.0
    default_price_6mo: float = 45.0
    default_price_year: float = 80.0
    default_btc_address: str = "btc:bc1q95njz0zu39chheehws5k22j5afhk48l0ffmphw"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def admin_ids_list(self) -> List[int]:
        if not self.admin_ids:
            return []
        return [int(id.strip()) for id in self.admin_ids.split(",") if id.strip()]

CURRENCY_SYMBOLS = {
    "NGN": "₦",
    "USD": "$",
    "EUR": "€"
}

settings = Settings()
