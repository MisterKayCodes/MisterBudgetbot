import aiosqlite
import asyncio
import config
from utils.helpers import get_current_datetime

async def migrate_database():
    print("Starting database migration...")
    db = await aiosqlite.connect(config.DATABASE_PATH)
    
    now = get_current_datetime()
    
    try:
        # Check and add missing columns to subscriptions table
        cursor = await db.execute("PRAGMA table_info(subscriptions)")
        columns = await cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'created_at' not in column_names:
            print("Adding created_at to subscriptions table...")
            await db.execute(f"ALTER TABLE subscriptions ADD COLUMN created_at TEXT DEFAULT '{now}'")
            print("✅ Added created_at column")
        
        if 'payment_method' not in column_names:
            print("Adding payment_method to subscriptions table...")
            await db.execute("ALTER TABLE subscriptions ADD COLUMN payment_method TEXT DEFAULT 'manual'")
            print("✅ Added payment_method column")
        
        # Check and add missing columns to trial_codes table
        cursor = await db.execute("PRAGMA table_info(trial_codes)")
        columns = await cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'duration_days' not in column_names and 'days' in column_names:
            print("Migrating days to duration_days in trial_codes table...")
            # Create new table with correct schema
            await db.execute("""
                CREATE TABLE IF NOT EXISTS trial_codes_new (
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
            # Copy data from old table (without relying on created_at)
            await db.execute(f"""
                INSERT INTO trial_codes_new (id, code, issued_by, duration_days, used, used_by, used_at, created_at)
                SELECT id, code, issued_by, 
                       COALESCE(days, 7) as duration_days,
                       CASE WHEN used_by IS NOT NULL THEN 1 ELSE 0 END as used,
                       used_by, used_at,
                       '{now}' as created_at
                FROM trial_codes
            """)
            # Drop old table and rename new one
            await db.execute("DROP TABLE trial_codes")
            await db.execute("ALTER TABLE trial_codes_new RENAME TO trial_codes")
            print("✅ Migrated trial_codes table")
        else:
            # Add missing columns individually
            if 'used' not in column_names:
                print("Adding used column to trial_codes table...")
                await db.execute("ALTER TABLE trial_codes ADD COLUMN used INTEGER DEFAULT 0")
                print("✅ Added used column")
            
            if 'created_at' not in column_names:
                print("Adding created_at to trial_codes table...")
                await db.execute(f"ALTER TABLE trial_codes ADD COLUMN created_at TEXT DEFAULT '{now}'")
                print("✅ Added created_at column to trial_codes")
        
        await db.commit()
        print("✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        await db.rollback()
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(migrate_database())
