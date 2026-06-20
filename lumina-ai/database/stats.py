import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "lumina.db")


def get_stats(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT xp, streak, sessions FROM stats WHERE username=?",
        (username,)
    )

    stats = cursor.fetchone()

    if stats is None:
        cursor.execute(
            "INSERT INTO stats VALUES (?, 0, 0, 0)",
            (username,)
        )
        conn.commit()
        stats = (0, 0, 0)

    conn.close()
    return stats


def add_xp(username, points):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO stats VALUES (?, 0, 0, 0)",
        (username,)
    )

    cursor.execute(
        "UPDATE stats SET xp = xp + ? WHERE username=?",
        (points, username)
    )

    conn.commit()
    conn.close()
