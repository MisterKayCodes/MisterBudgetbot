import aiosqlite
import config
from pathlib import Path

async def get_db():
    Path(config.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    db = await aiosqlite.connect(config.DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    return db

async def init_database():
    db = await get_db()
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            currency TEXT DEFAULT 'NGN',
            spending_percent INTEGER DEFAULT 60,
            savings_percent INTEGER DEFAULT 20,
            business_percent INTEGER DEFAULT 20,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,
            account_name TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            account_type TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL DEFAULT 0.0,
            auto_save_percent INTEGER DEFAULT 0,
            deadline TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reminder_type TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            time TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_type TEXT NOT NULL,
            price REAL DEFAULT 0.0,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            is_trial INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            payment_method TEXT DEFAULT 'manual',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS trial_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            issued_by INTEGER,
            duration_days INTEGER DEFAULT 7,
            used INTEGER DEFAULT 0,
            used_by INTEGER DEFAULT NULL,
            used_at TEXT DEFAULT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS pending_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_type TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_address TEXT,
            screenshot_file_id TEXT,
            status TEXT DEFAULT 'pending',
            admin_note TEXT DEFAULT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    await db.execute("""
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            subscription_mode INTEGER DEFAULT 0,
            default_trial_days INTEGER DEFAULT 7,
            monthly_price REAL DEFAULT 10.0,
            price_3mo REAL DEFAULT 25.0,
            price_6mo REAL DEFAULT 45.0,
            price_year REAL DEFAULT 80.0,
            btc_address TEXT DEFAULT 'BTC_DUMMY_ADDR_XXXXXXXXXXXXXXXX',
            usdt_trc20_address TEXT DEFAULT '',
            bank_account_info TEXT DEFAULT ''
        )
    """)
    
    await db.execute("INSERT OR IGNORE INTO admin_settings (id) VALUES (1)")
    
    await db.commit()
    await db.close()
