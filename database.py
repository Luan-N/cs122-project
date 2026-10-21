from datetime import date

import sqlitecloud
from env import DATABASE_URL


def get_db_connection():
    return sqlitecloud.connect(DATABASE_URL)


def add_transaction(user_id, amount, category, payment_method=None,
                    transaction_date=None, description=None):
    transaction_date = transaction_date or date.today().isoformat()
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO transactions
                (user_id, amount, category, payment_method, transaction_date, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, payment_method, transaction_date, description)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_transaction(user_id, transaction_id):
    conn = get_db_connection()
    try:
        return conn.execute(
            """
            SELECT transaction_id, amount, category, payment_method, transaction_date, description
            FROM transactions
            WHERE transaction_id = ? AND user_id = ?
            """,
            (transaction_id, user_id)
        ).fetchone()
    finally:
        conn.close()


def update_transaction(user_id, transaction_id, amount, category,
                       payment_method=None, transaction_date=None, description=None):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """
            UPDATE transactions
            SET amount = ?, category = ?, payment_method = ?,
                transaction_date = ?, description = ?
            WHERE transaction_id = ? AND user_id = ?
            """,
            (amount, category, payment_method, transaction_date, description,
             transaction_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_transactions(user_id):
    ''' This method shows record of transactions'''
    conn = get_db_connection()
    try:
        rows = conn.execute(
            """
            SELECT transaction_id, transaction_date, amount, category, payment_method, description
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchall()

        return rows

    finally:
        conn.close()


def track_spending(user_id):
    '''Show total income, expenses, and balance for the user.'''
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
        bar_length = int((v / val) * 40) if val else 0
        print(f"\n{k.ljust(10)} {bar * bar_length} {v}")