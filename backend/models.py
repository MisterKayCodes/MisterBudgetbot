from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: int
    full_name: str
    email: EmailStr

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    currency: Optional[str] = None
    spending_percent: Optional[int] = None
    savings_percent: Optional[int] = None
    business_percent: Optional[int] = None

class User(BaseModel):
    id: int
    telegram_id: int
    full_name: str
    email: str
    currency: str
    spending_percent: int
    savings_percent: int
    business_percent: int
    created_at: datetime
    updated_at: datetime

class IncomeCreate(BaseModel):
    amount: float

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str

class GoalCreate(BaseModel):
    goal_name: str
    target_amount: float
    deadline: Optional[str] = None
    auto_save_percent: int = 0

class Goal(BaseModel):
    id: int
    user_id: int
    goal_name: str
    target_amount: float
    current_amount: float
    auto_save_percent: int
    deadline: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class Account(BaseModel):
    id: int
    user_id: int
    account_type: str
    account_name: str
    balance: float
    created_at: datetime
    updated_at: datetime

class Transaction(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    category: Optional[str]
    description: Optional[str]
    account_type: Optional[str]
    created_at: datetime

class SettingsUpdate(BaseModel):
    currency: Optional[str] = None
    spending_percent: Optional[int] = None
    savings_percent: Optional[int] = None
    business_percent: Optional[int] = None

class TrialCodeRedeem(BaseModel):
    code: str

class TrialCodeGenerate(BaseModel):
    duration_days: int

class ReminderToggle(BaseModel):
    reminder_type: str
