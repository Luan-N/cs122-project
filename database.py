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
    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT transaction_id, amount, category, payment_method, transaction_date, description
        FROM transactions
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()

    conn.close()
    return rows
