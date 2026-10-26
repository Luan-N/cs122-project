import sqlitecloud
from env import DATABASE_URL
from datetime import date
import calendar


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
    """ This method shows record of transactions in a month """

    today = date.today()
    month = today.month
    year = today.year

    startDate = date(year, month, 1).strftime('%Y-%m-%d')
    last_day = calendar.monthrange(year, month)[1]
    endDate = date(year, month, last_day).strftime('%Y-%m-%d') 

    conn = get_db_connection()
    try:
        rows = conn.execute(
            """
            SELECT transaction_id, transaction_date, category, payment_method, description, amount
            FROM transactions
            WHERE user_id = ? AND transaction_date BETWEEN ? AND ?
            """,
            (user_id, startDate, endDate)
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
            SELECT SUM(amount) AS expenses
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

def delete_transaction(user_id, transaction_id):
    """ Delete the transaction from the database."""

    conn = get_db_connection()
    try:
        rows = conn.execute(
            """
            DELETE FROM transactions
            WHERE user_id = ? AND transaction_id = ?
            """, (user_id, transaction_id)
        )
        conn.commit()
        return rows.rowcount > 0

    finally:
        conn.close()

def search_transaction(user_id, mdate):
    """ Search the transaction on specific month from the database """

    conn = get_db_connection()
    try:
        rows = conn.execute(
            """
            SELECT transaction_id, transaction_date, category, payment_method, description, amount
            FROM transactions
            WHERE user_id = ? AND transaction_date LIKE ?
            """, (user_id, f"{mdate}%")
        ).fetchall()
        return rows
    finally:
        conn.close()
