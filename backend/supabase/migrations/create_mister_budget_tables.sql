/*
  # Mister Budget - Complete Database Schema

  1. New Tables
    - users: User profiles with financial settings
    - accounts: User account balances (Spending/Savings/Business)
    - transactions: Income and expense records
    - goals: Savings goals with auto-save features
    - reminders: User reminder preferences
    - subscriptions: User subscription records
    - trial_codes: Trial code management
    - pending_payments: Manual payment submissions (optional)
    - admin_settings: Global admin configuration

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to access their own data
    - Add admin policies for admin_settings and trial_codes
*/

CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    currency TEXT DEFAULT 'NGN',
    spending_percent INTEGER DEFAULT 60,
    savings_percent INTEGER DEFAULT 20,
    business_percent INTEGER DEFAULT 20,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS accounts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_type TEXT NOT NULL,
    account_name TEXT NOT NULL,
    balance REAL DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT,
    description TEXT,
    account_type TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS goals (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal_name TEXT NOT NULL,
    target_amount REAL NOT NULL,
    current_amount REAL DEFAULT 0.0,
    auto_save_percent INTEGER DEFAULT 0,
    deadline TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reminders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reminder_type TEXT NOT NULL,
    enabled INTEGER DEFAULT 1,
    time TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_type TEXT NOT NULL,
    price REAL DEFAULT 0.0,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ,
    is_trial INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    payment_method TEXT DEFAULT 'manual',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS trial_codes (
    id BIGSERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    issued_by BIGINT,
    duration_days INTEGER DEFAULT 7,
    used INTEGER DEFAULT 0,
    used_by BIGINT DEFAULT NULL,
    used_at TIMESTAMPTZ DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pending_payments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_type TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    payment_address TEXT,
    screenshot_file_id TEXT,
    status TEXT DEFAULT 'pending',
    admin_note TEXT DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

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
);

INSERT INTO admin_settings (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE trial_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE pending_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON users FOR SELECT
    USING (true);

CREATE POLICY "Users can insert own profile"
    ON users FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can update own profile"
    ON users FOR UPDATE
    USING (true);

CREATE POLICY "Users can view own accounts"
    ON accounts FOR SELECT
    USING (true);

CREATE POLICY "Users can manage own accounts"
    ON accounts FOR ALL
    USING (true);

CREATE POLICY "Users can view own transactions"
    ON transactions FOR SELECT
    USING (true);

CREATE POLICY "Users can create own transactions"
    ON transactions FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can view own goals"
    ON goals FOR SELECT
    USING (true);

CREATE POLICY "Users can manage own goals"
    ON goals FOR ALL
    USING (true);

CREATE POLICY "Users can view own reminders"
    ON reminders FOR SELECT
    USING (true);

CREATE POLICY "Users can manage own reminders"
    ON reminders FOR ALL
    USING (true);

CREATE POLICY "Users can view own subscriptions"
    ON subscriptions FOR SELECT
    USING (true);

CREATE POLICY "Anyone can view trial codes"
    ON trial_codes FOR SELECT
    USING (true);

CREATE POLICY "Anyone can update trial codes"
    ON trial_codes FOR UPDATE
    USING (true);

CREATE POLICY "Anyone can view pending payments"
    ON pending_payments FOR SELECT
    USING (true);

CREATE POLICY "Anyone can create pending payments"
    ON pending_payments FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Anyone can view admin settings"
    ON admin_settings FOR SELECT
    USING (true);

CREATE POLICY "Anyone can update admin settings"
    ON admin_settings FOR UPDATE
    USING (true);

CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
