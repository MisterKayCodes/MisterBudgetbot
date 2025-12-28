import aiohttp
from typing import Optional, Dict, Any
from config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        session = await self.get_session()
        url = f"{self.base_url}{endpoint}"

        async with session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                error_detail = await response.text()
                raise Exception(f"API Error {response.status}: {error_detail}")
            return await response.json()

    async def register_user(self, telegram_id: int, full_name: str, email: str):
        return await self._request("POST", "/users/", json={
            "telegram_id": telegram_id,
            "full_name": full_name,
            "email": email
        })

    async def get_user(self, telegram_id: int):
        try:
            return await self._request("GET", f"/users/{telegram_id}")
        except:
            return None

    async def update_user(self, telegram_id: int, updates: Dict):
        return await self._request("PATCH", f"/users/{telegram_id}", json=updates)

    async def add_income(self, telegram_id: int, amount: float):
        return await self._request("POST", f"/income/{telegram_id}", json={"amount": amount})

    async def get_income_history(self, telegram_id: int, limit: int = 10):
        return await self._request("GET", f"/income/{telegram_id}?limit={limit}")

    async def add_expense(self, telegram_id: int, description: str, amount: float, category: str):
        return await self._request("POST", f"/expenses/{telegram_id}", json={
            "description": description,
            "amount": amount,
            "category": category
        })

    async def get_expense_history(self, telegram_id: int, limit: int = 10):
        return await self._request("GET", f"/expenses/{telegram_id}?limit={limit}")

    async def create_goal(self, telegram_id: int, goal_name: str, target_amount: float, deadline: Optional[str] = None, auto_save_percent: int = 0):
        return await self._request("POST", f"/goals/{telegram_id}", json={
            "goal_name": goal_name,
            "target_amount": target_amount,
            "deadline": deadline,
            "auto_save_percent": auto_save_percent
        })

    async def get_active_goals(self, telegram_id: int):
        return await self._request("GET", f"/goals/{telegram_id}/active")

    async def get_completed_goals(self, telegram_id: int):
        return await self._request("GET", f"/goals/{telegram_id}/completed")

    async def get_accounts(self, telegram_id: int):
        return await self._request("GET", f"/accounts/{telegram_id}")

    async def get_total_balance(self, telegram_id: int):
        return await self._request("GET", f"/accounts/{telegram_id}/balance")

    async def get_weekly_summary(self, telegram_id: int):
        return await self._request("GET", f"/summary/{telegram_id}/weekly")

    async def get_monthly_summary(self, telegram_id: int):
        return await self._request("GET", f"/summary/{telegram_id}/monthly")

    async def get_alltime_summary(self, telegram_id: int):
        return await self._request("GET", f"/summary/{telegram_id}/alltime")

    async def get_spending_analysis(self, telegram_id: int):
        return await self._request("GET", f"/advisor/{telegram_id}/spending")

    async def get_savings_analysis(self, telegram_id: int):
        return await self._request("GET", f"/advisor/{telegram_id}/savings")

    async def get_recommendations(self, telegram_id: int):
        return await self._request("GET", f"/advisor/{telegram_id}/recommendations")

    async def get_reminders(self, telegram_id: int):
        return await self._request("GET", f"/reminders/{telegram_id}")

    async def toggle_reminder(self, telegram_id: int, reminder_type: str):
        return await self._request("POST", f"/reminders/{telegram_id}/toggle", json={
            "reminder_type": reminder_type
        })

    async def get_subscription_status(self, telegram_id: int):
        return await self._request("GET", f"/subscription/{telegram_id}/status")

    async def redeem_trial_code(self, telegram_id: int, code: str):
        return await self._request("POST", f"/subscription/{telegram_id}/redeem", json={
            "code": code
        })

    async def toggle_subscription_mode(self, telegram_id: int):
        return await self._request("POST", f"/admin/subscription-mode/{telegram_id}")

    async def generate_trial_code(self, telegram_id: int, duration_days: int):
        return await self._request("POST", f"/admin/trial-code/{telegram_id}", json={
            "duration_days": duration_days
        })

    async def get_subscribers(self, telegram_id: int):
        return await self._request("GET", f"/admin/subscribers/{telegram_id}")

    async def get_statistics(self, telegram_id: int):
        return await self._request("GET", f"/admin/statistics/{telegram_id}")

    async def get_all_users(self, telegram_id: int):
        return await self._request("GET", f"/admin/users/{telegram_id}")

    async def delete_all_users(self, telegram_id: int):
        return await self._request("DELETE", f"/admin/users/{telegram_id}")

api_client = APIClient()
