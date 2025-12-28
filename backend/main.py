from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, income, expenses, goals, accounts, summary, advisor, reminders, subscription, admin

app = FastAPI(title="Mister Budget API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(income.router, prefix="/api/income", tags=["Income"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["Accounts"])
app.include_router(summary.router, prefix="/api/summary", tags=["Summary"])
app.include_router(advisor.router, prefix="/api/advisor", tags=["Advisor"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Mister Budget API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
