from database import get_db
from database_models.users import get_user_by_telegram_id
from database_models.accounts import get_account_by_type
from datetime import datetime, timedelta
from typing import Optional
import csv
import io

async def get_period_summary(user_id: int, days: Optional[int] = None):
    db = await get_db()
    
    if days:
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        cursor = await db.execute(
            """SELECT transaction_type, category, SUM(amount) as total, COUNT(*) as count
               FROM transactions 
               WHERE user_id = ? AND created_at >= ?
               GROUP BY transaction_type, category""",
            (user_id, start_date)
        )
    else:
        cursor = await db.execute(
            """SELECT transaction_type, category, SUM(amount) as total, COUNT(*) as count
               FROM transactions 
               WHERE user_id = ?
               GROUP BY transaction_type, category""",
            (user_id,)
        )
    
    summary = await cursor.fetchall()
    await db.close()
    
    income_total = sum(row['total'] for row in summary if row['transaction_type'] == 'income')
    expense_total = sum(row['total'] for row in summary if row['transaction_type'] == 'expense')
    
    expense_by_category = {}
    for row in summary:
        if row['transaction_type'] == 'expense':
            expense_by_category[row['category']] = {
                'total': row['total'],
                'count': row['count']
            }
    
    return {
        'income_total': income_total,
        'expense_total': expense_total,
        'net': income_total - expense_total,
        'expense_by_category': expense_by_category,
        'transaction_count': sum(row['count'] for row in summary)
    }

async def generate_csv_export(telegram_id: int) -> Optional[str]:
    user = await get_user_by_telegram_id(telegram_id)
    
    if not user:
        return None
    
    db = await get_db()
    cursor = await db.execute(
        """SELECT transaction_type, amount, category, description, created_at
           FROM transactions 
           WHERE user_id = ?
           ORDER BY created_at DESC""",
        (user['id'],)
    )
    
    transactions = await cursor.fetchall()
    await db.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Date', 'Type', 'Amount', 'Category', 'Description'])
    
    for txn in transactions:
        writer.writerow([
            txn['created_at'],
            txn['transaction_type'].capitalize(),
            txn['amount'],
            txn['category'],
            txn['description'] or ''
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    filename = f"mister_budget_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w') as f:
        f.write(csv_content)
    
    return filename
