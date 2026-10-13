import sqlitecloud
from env import DATABASE_URL


def get_db_connection():
    return sqlitecloud.connect(DATABASE_URL)

def get_transactions(user_id):
    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM transactions
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()

    conn.close()
    return rows