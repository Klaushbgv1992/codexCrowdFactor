from __future__ import annotations

import sqlite3


class Repository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert_reading(self, payload: dict) -> None:
        self.conn.execute(
            """INSERT INTO crowd_readings(timestamp,scene_id,person_count,car_count,crowd_factor,stream_status)
            VALUES(:timestamp,:scene_id,:person_count,:car_count,:crowd_factor,:stream_status)""",
            payload,
        )
        self.conn.commit()

    def current_by_scene(self) -> dict:
        rows = self.conn.execute(
            """SELECT r.* FROM crowd_readings r
               JOIN (SELECT scene_id, MAX(timestamp) AS ts FROM crowd_readings GROUP BY scene_id) x
               ON r.scene_id=x.scene_id AND r.timestamp=x.ts"""
        ).fetchall()
        return {row["scene_id"]: dict(row) for row in rows}

    def latest(self) -> dict | None:
        row = self.conn.execute("SELECT * FROM crowd_readings ORDER BY timestamp DESC LIMIT 1").fetchone()
        return dict(row) if row else None

    def history(self, hours: int):
        return [
            dict(r)
            for r in self.conn.execute(
                "SELECT timestamp,scene_id,person_count,car_count,crowd_factor FROM crowd_readings WHERE timestamp >= datetime('now', ?) ORDER BY timestamp",
                (f"-{hours} hours",),
            ).fetchall()
        ]
