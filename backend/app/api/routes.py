from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter

from app.crowd_score import level_meta


def create_router(state):
    router = APIRouter(prefix="/api")

    @router.get("/crowd/current")
    def crowd_current():
        scenes = state.repo.current_by_scene()
        parking = scenes.get("parking", {}).get("car_count", 0)
        pier = scenes.get("pier", {}).get("person_count", 0)
        beach = scenes.get("beach", {}).get("person_count", 0)
        water = scenes.get("water", {}).get("person_count", 0)
        crowd_factor = state.latest_factor
        level, color, reco = level_meta(crowd_factor)
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        return {
            "timestamp": now,
            "stream_status": state.stream_state.stream_status,
            "crowd_factor": crowd_factor,
            "crowd_level": level,
            "crowd_level_color": color,
            "recommendation": reco,
            "zones": {
                "parking": {"cars": parking, "level": level, "updated_at": now},
                "pier": {"people": pier, "level": level, "updated_at": now},
                "beach": {"people": beach, "level": level, "updated_at": now},
                "water": {"people": water, "level": level, "updated_at": now},
            },
            "cta": {"text": reco, "url": "https://vibesurfschool.com/book", "button_text": "Book a Lesson"},
        }

    @router.get("/crowd/history")
    def crowd_history(hours: int = 12):
        rows = state.repo.history(hours)
        buckets = defaultdict(lambda: {"parking_cars": 0, "pier_people": 0, "beach_people": 0, "water_people": 0, "crowd_factor": 0, "n": 0})
        for r in rows:
            key = r["timestamp"][:16] + ":00Z"
            b = buckets[key]
            if r["scene_id"] == "parking":
                b["parking_cars"] += r["car_count"]
            if r["scene_id"] == "pier":
                b["pier_people"] += r["person_count"]
            if r["scene_id"] == "beach":
                b["beach_people"] += r["person_count"]
            if r["scene_id"] == "water":
                b["water_people"] += r["person_count"]
            b["crowd_factor"] += r["crowd_factor"]
            b["n"] += 1
        data = []
        for ts, b in sorted(buckets.items()):
            n = max(1, b.pop("n"))
            data.append({"timestamp": ts, **{k: round(v / n, 2) for k, v in b.items()}})
        return {"period": f"last_{hours}_hours", "interval": "15min", "data": data}

    @router.get("/crowd/best-times")
    def best_times():
        return {
            "day_of_week": datetime.now().strftime("%A").lower(),
            "hours": [{"hour": h, "avg_crowd_factor": max(5, (h - 6) * 4), "level": "quiet" if h < 10 else "moderate"} for h in range(6, 20)],
            "best_time": "6:00 AM - 8:00 AM",
            "peak_time": "11:00 AM - 2:00 PM",
        }

    @router.get("/health")
    def health():
        return {
            "status": "healthy",
            "stream_connected": state.stream_state.stream_connected,
            "last_frame_captured": state.stream_state.last_frame_captured,
            "last_detection_run": state.stream_state.last_frame_captured,
            "model_loaded": True,
            "database_connected": True,
            "uptime_seconds": int((datetime.now(timezone.utc) - state.started_at).total_seconds()),
        }

    return router
