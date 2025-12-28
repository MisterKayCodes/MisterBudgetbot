# Mister Budget - Complete Setup Guide

This guide will walk you through setting up all three components of the Mister Budget application.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- A Supabase account (free tier is fine)
- A Telegram account and bot token (if using the Telegram bot)

## Step-by-Step Setup

### 1. Setup Supabase Database

1. Create a new project at https://supabase.com
2. Go to **SQL Editor** in your Supabase dashboard
3. Create a new query and paste the contents of `backend/supabase/migrations/create_mister_budget_tables.sql`
4. Run the query to create all tables and policies
5. Note down your project credentials:
   - Project URL (looks like: https://xxxxx.supabase.co)
   - Anon/Public Key
   - Service Role Key (keep this secret!)

### 2. Setup FastAPI Backend

```bash
cd backend

pip install -r requirements.txt

cp .env.example .env
```

Edit the `.env` file with your credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here

JWT_SECRET_KEY=generate_a_random_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

ADMIN_IDS=your_telegram_id

DEFAULT_CURRENCY=NGN
DEFAULT_SPENDING_PERCENT=60
DEFAULT_SAVINGS_PERCENT=20
DEFAULT_BUSINESS_PERCENT=20
```

Start the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be running at http://localhost:8000
API documentation at http://localhost:8000/docs

### 3. Setup Telegram Bot (Optional)

If you want to use the Telegram interface:

```bash
cd telegram-bot

pip install -r requirements.txt

cp .env.example .env
```

Get your bot token:
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
API_BASE_URL=http://localhost:8000/api
```

Start the bot:
```bash
python bot.py
```

Find your Telegram ID:
- Message @userinfobot on Telegram to get your ID
- Add this ID to the backend's `.env` file in `ADMIN_IDS`

### 4. Setup React Frontend

```bash
cd frontend

npm install

cp .env.example .env
```

Edit `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Start the development server:
```bash
npm run dev
```

The web app will be running at http://localhost:3000

## Running the Complete Stack

You need three terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Telegram Bot (Optional):**
```bash
cd telegram-bot
python bot.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

## Using the Application

### Web Interface

1. Open http://localhost:3000 in your browser
2. Click "Register" if you're a new user
3. Enter your Telegram ID (get it from @userinfobot), name, and email
4. Login with your Telegram ID
5. Start managing your finances!

### Telegram Bot

1. Find your bot on Telegram (search for the username you gave it)
2. Send `/start` to begin
3. Complete the onboarding process
4. Use the interactive menu

## Troubleshooting

### Backend won't start
- Check that all environment variables are set correctly
- Verify Supabase credentials are correct
- Make sure port 8000 is not already in use

### Telegram bot not responding
- Verify bot token is correct
- Check that the backend is running
- Look for error messages in the bot console

### Frontend errors
- Make sure backend is running first
- Check that API_BASE_URL is correct in `.env`
- Clear browser cache and localStorage

### Database errors
- Verify the migration was run successfully in Supabase
- Check RLS policies are enabled
- Ensure you're using the service role key for the backend

## Next Steps

- Add more users through the web interface or Telegram bot
- Explore the admin features (if your Telegram ID is in ADMIN_IDS)
- Customize settings like currency and income split percentages
- Set up savings goals and track progress
- Review financial insights in the Advisor section

## Production Deployment

For production deployment:
1. Use production Supabase instance
2. Set secure JWT secret keys
3. Deploy backend to Railway, Render, or similar
4. Deploy frontend to Vercel, Netlify, or similar
5. Run Telegram bot on a VPS with PM2 or systemd
6. Enable HTTPS for all services
7. Update CORS settings in backend for production domains

## Support

- Check individual README files in each directory
- Review API documentation at http://localhost:8000/docs
- Examine code comments and structure

---

Enjoy managing your budget with Mister Budget!
