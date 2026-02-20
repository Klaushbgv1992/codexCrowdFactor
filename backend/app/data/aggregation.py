from __future__ import annotations

import sqlite3


def cleanup(conn: sqlite3.Connection, retention_days: int) -> None:
    conn.execute("DELETE FROM crowd_readings WHERE timestamp < datetime('now', ?)", (f"-{retention_days} days",))
    conn.commit()
