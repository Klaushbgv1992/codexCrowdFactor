from __future__ import annotations

import sqlite3


def init_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS crowd_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            scene_id TEXT NOT NULL,
            person_count INTEGER DEFAULT 0,
            car_count INTEGER DEFAULT 0,
            crowd_factor INTEGER DEFAULT 0,
            stream_status TEXT DEFAULT 'online',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON crowd_readings(timestamp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_scene ON crowd_readings(scene_id)")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS crowd_history_15min (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bucket_start TEXT NOT NULL,
            parking_cars_avg REAL DEFAULT 0,
            pier_people_avg REAL DEFAULT 0,
            beach_people_avg REAL DEFAULT 0,
            water_people_avg REAL DEFAULT 0,
            crowd_factor_avg REAL DEFAULT 0,
            reading_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bucket ON crowd_history_15min(bucket_start)")
    conn.commit()
    return conn
