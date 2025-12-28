# Mister Budget - Telegram Bot

Telegram bot interface for Mister Budget that connects to the FastAPI backend.

## Features

- User onboarding and registration
- Income and expense management
- Savings goals tracking
- Financial advisor insights
- Reports and summaries
- Settings management
- Multi-currency support

## Setup

### 1. Install Dependencies

```bash
cd telegram-bot
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Required variables:
- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather
- `API_BASE_URL` - URL of your FastAPI backend (default: http://localhost:8000/api)

### 3. Start the Bot

Make sure the FastAPI backend is running first, then:

```bash
python bot.py
```

## Project Structure

```
telegram-bot/
├── bot.py              # Main bot entry point
├── config.py           # Configuration
├── api_client.py       # API client for backend communication
├── handlers/           # Message and callback handlers
│   ├── start.py       # Onboarding
│   ├── income.py      # Income management
│   ├── expense.py     # Expense tracking
│   ├── goals.py       # Goals management
│   ├── summary.py     # Reports
│   ├── advisor.py     # Financial advisor
│   ├── settings.py    # Settings
│   ├── accounts.py    # Account viewing
│   └── reminders.py   # Reminder settings
├── keyboards/          # Inline keyboard layouts
├── states/            # FSM states for conversations
└── utils/             # Utility functions
```

## Bot Commands

- `/start` - Start the bot and register

## Usage

1. Start a conversation with your bot on Telegram
2. Send `/start` to begin onboarding
3. Enter your name and email
4. Use the interactive menu to manage your finances

## Development

The bot uses:
- **aiogram 3.4.1** - Modern Telegram Bot framework
- **aiohttp** - Async HTTP client for API calls
- **FSM** - Finite State Machine for conversation flows

## Notes

- The bot communicates with the FastAPI backend via HTTP
- All data is stored in Supabase through the backend
- Make sure the backend is running before starting the bot

## License

Private project
