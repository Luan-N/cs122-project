from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from database import get_db_connection

ph = PasswordHasher()

def signup(username, password):
    password_hash = ph.hash(password)

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        conn.close()


def login(username, password):
    conn = get_db_connection()

    try:
        user = conn.execute(
            """
            SELECT user_id, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

    finally:
        conn.close()

    if user is None:
        return None

    user_id, password_hash = user

    try:
        ph.verify(password_hash, password)
        return user_id
    except VerifyMismatchError:
        return None