# Mister Budget - FastAPI Backend

RESTful API backend for Mister Budget application using FastAPI and Supabase.

## Features

- User management and authentication
- Income and expense tracking
- Savings goals with auto-save
- Financial advisor and analytics
- Subscription management with trial codes
- Admin panel for managing users and settings
- Multi-currency support

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database with real-time capabilities
- **Pydantic** - Data validation
- **Python 3.11+**

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Required variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key
- `SUPABASE_SERVICE_KEY` - Your Supabase service role key

### 3. Run Database Migrations

Go to your Supabase project dashboard and run the SQL migration file located at:
`supabase/migrations/create_mister_budget_tables.sql`

### 4. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/{telegram_id}` - Get user profile
- `PATCH /api/users/{telegram_id}` - Update user settings

### Income
- `POST /api/income/{telegram_id}` - Add income
- `GET /api/income/{telegram_id}` - Get income history

### Expenses
- `POST /api/expenses/{telegram_id}` - Add expense
- `GET /api/expenses/{telegram_id}` - Get expense history

### Goals
- `POST /api/goals/{telegram_id}` - Create goal
- `GET /api/goals/{telegram_id}/active` - List active goals
- `GET /api/goals/{telegram_id}/completed` - List completed goals

### Accounts
- `GET /api/accounts/{telegram_id}` - List all accounts
- `GET /api/accounts/{telegram_id}/balance` - Get total balance

### Summary
- `GET /api/summary/{telegram_id}/weekly` - Weekly summary
- `GET /api/summary/{telegram_id}/monthly` - Monthly summary
- `GET /api/summary/{telegram_id}/alltime` - All-time summary
- `GET /api/summary/{telegram_id}/export` - Export CSV

### Advisor
- `GET /api/advisor/{telegram_id}/spending` - Spending analysis
- `GET /api/advisor/{telegram_id}/savings` - Savings analysis
- `GET /api/advisor/{telegram_id}/recommendations` - Get recommendations

### Reminders
- `GET /api/reminders/{telegram_id}` - Get reminder settings
- `POST /api/reminders/{telegram_id}/toggle` - Toggle reminder

### Subscription
- `GET /api/subscription/{telegram_id}/status` - Check subscription status
- `POST /api/subscription/{telegram_id}/redeem` - Redeem trial code

### Admin (Requires admin telegram_id)
- `POST /api/admin/subscription-mode/{telegram_id}` - Toggle subscription mode
- `POST /api/admin/trial-code/{telegram_id}` - Generate trial code
- `GET /api/admin/subscribers/{telegram_id}` - List subscribers
- `GET /api/admin/statistics/{telegram_id}` - Get bot statistics
- `GET /api/admin/users/{telegram_id}` - List all users
- `DELETE /api/admin/users/{telegram_id}` - Delete all users

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and settings
├── database.py            # Supabase client setup
├── models.py              # Pydantic models
├── routers/               # API route handlers
│   ├── users.py
│   ├── income.py
│   ├── expenses.py
│   ├── goals.py
│   ├── accounts.py
│   ├── summary.py
│   ├── advisor.py
│   ├── reminders.py
│   ├── subscription.py
│   └── admin.py
├── services/              # Business logic
│   ├── user_service.py
│   ├── income_service.py
│   ├── expense_service.py
│   ├── goals_service.py
│   ├── accounts_service.py
│   ├── summary_service.py
│   ├── advisor_service.py
│   ├── reminders_service.py
│   ├── subscription_service.py
│   └── admin_service.py
└── supabase/
    └── migrations/
        └── create_mister_budget_tables.sql
```

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload
```

## Production

Run with Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Security Notes

- All endpoints use Supabase RLS policies for data security
- Admin endpoints check telegram_id against ADMIN_IDS list
- CORS is enabled for all origins (configure for production)
- Use HTTPS in production

## License

Private project
