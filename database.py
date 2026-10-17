import sqlitecloud
from env import DATABASE_URL
from tabulate import tabulate


def get_db_connection():
    return sqlitecloud.connect(DATABASE_URL)

def get_transactions(user_id):
    ''' This method shows record of transactions'''
    conn = get_db_connection()
    try:
        rows = conn.execute(
            """
            SELECT transaction_date, description, payment_method, transaction_Id, amount 
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchall()

        return rows
    
    finally:
        conn.close()

def track_spending(user_id):
    ''' This method allow users to see  their income and expenses each month'''
    conn = get_db_connection()
    try:
        income_row = conn.execute(
            """
            SELECT SUM(amount) AS income
            FROM transactions
            WHERE amount > 0 AND user_id = ?
            """, (user_id,)
        ).fetchone()

        expenses_row = conn.execute(
            """
            SELECT SUM(amount) AS income
            FROM transactions
            WHERE amount < 0 AND user_id = ?
            """, (user_id,)
        ).fetchone()

        income = income_row[0] if income_row and income_row[0] is not None else 0
        expenses = expenses_row[0] if expenses_row and expenses_row[0] is not None else 0
        
        balance = income + expenses

        return [[income, abs(expenses), balance]]

    except Exception as e:
        print(e)
        return None

    finally:
        conn.close()

def print_cash_flow(income, expenses):
    data = {"Income": income, "Expenses": expenses}
    bar = "█"
    val = max(data.values())
    for k, v in data.items():
        bar_length = int((v / val) * 40)
        print(f"\n{k.ljust(10)} {bar * bar_length} {v}")