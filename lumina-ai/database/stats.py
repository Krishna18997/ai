import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "lumina.db")


def add_xp(username, xp_to_add):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        total_sessions INTEGER DEFAULT 0,
        last_active_date TEXT
    )
    """)

    cursor.execute(
        "SELECT * FROM study_stats WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.execute(
            """
            INSERT INTO study_stats
            (username, xp, streak, total_sessions)
            VALUES (?, ?, ?, ?)
            """,
            (username, xp_to_add, 0, 1)
        )
    else:
        cursor.execute(
            """
            UPDATE study_stats
            SET xp = xp + ?,
                total_sessions = total_sessions + 1
            WHERE username = ?
            """,
            (xp_to_add, username)
        )

    conn.commit()
    conn.close()


def get_stats(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        total_sessions INTEGER DEFAULT 0,
        last_active_date TEXT
    )
    """)

    cursor.execute(
        """
        SELECT xp, streak, total_sessions
        FROM study_stats
        WHERE username=?
        """,
        (username,)
    )

    stats = cursor.fetchone()

    if stats is None:
        cursor.execute(
            """
            INSERT INTO study_stats
            (username, xp, streak, total_sessions)
            VALUES (?, 0, 0, 0)
            """,
            (username,)
        )
        conn.commit()
        stats = (0, 0, 0)

    conn.close()
    return stats
