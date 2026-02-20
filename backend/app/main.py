from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import cv2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app.api.routes import create_router
from app.capture.reconnect import next_backoff
from app.capture.stream import StreamState, YouTubeFrameCapture, now_iso
from app.config import scenes, settings
from app.crowd_score import calculate_crowd_factor
from app.data.aggregation import cleanup
from app.data.models import init_db
from app.data.repository import Repository
from app.vision.detector import Detector
from app.vision.scene_classifier import SceneClassifier
from app.vision.stabilizer import CountStabilizer


@dataclass
class AppState:
    repo: Repository
    stream_state: StreamState
    latest_factor: int
    started_at: datetime


cfg = settings()
scene_cfg = scenes()
conn = init_db(cfg["storage"]["sqlite_path"])
state = AppState(repo=Repository(conn), stream_state=StreamState(), latest_factor=0, started_at=datetime.now(timezone.utc))

app = FastAPI(title="Dania Beach Crowd Checker")
app.add_middleware(CORSMiddleware, allow_origins=cfg["api"]["cors_origins"], allow_methods=["*"], allow_headers=["*"])
app.include_router(create_router(state))


async def worker() -> None:
    capture = YouTubeFrameCapture(cfg["stream"]["youtube_url"], cfg["stream"]["url_refresh_interval_seconds"])
    classifier = SceneClassifier(scene_cfg, cfg["scene_classifier"]["similarity_threshold"])
    detector = Detector()
    stabilizer = CountStabilizer(cfg["stabilization"]["window_seconds"])
    backoff = 1
    while True:
        try:
            frame = capture.capture_frame()
            state.stream_state.stream_connected = True
            state.stream_state.stream_status = "online"
            state.stream_state.last_frame_captured = now_iso()
            pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            scene_id = classifier.classify(pil)
            if scene_id == "transitioning" or scene_cfg["scenes"].get(scene_id, {}).get("skip_detection"):
                await asyncio.sleep(cfg["stream"]["capture_interval_seconds"])
                continue
            counts = detector.detect(frame, scene_cfg["scenes"].get(scene_id, {}))
            ts = int(time.time())
            key = "parking" if scene_id == "parking" else scene_id
            metric = counts["car_count"] if scene_id == "parking" else counts["person_count"]
            stabilizer.add_reading(key, ts, metric)
            crowd_factor = calculate_crowd_factor(
                stabilizer.get_stable_count("parking"),
                stabilizer.get_stable_count("pier"),
                stabilizer.get_stable_count("beach"),
                stabilizer.get_stable_count("water"),
                cfg,
            )
            state.latest_factor = crowd_factor
            state.repo.insert_reading({
                "timestamp": now_iso(),
                "scene_id": scene_id,
                "person_count": counts["person_count"],
                "car_count": counts["car_count"],
                "crowd_factor": crowd_factor,
                "stream_status": "online",
            })
            cleanup(conn, cfg["storage"]["retention_days"])
            backoff = 1
            await asyncio.sleep(cfg["stream"]["capture_interval_seconds"])
        except Exception as exc:
            state.stream_state.stream_connected = False
            state.stream_state.stream_status = "offline"
            state.stream_state.last_error = str(exc)
            await asyncio.sleep(max(60, backoff))
            backoff = next_backoff(backoff, cfg["stream"]["reconnect_max_backoff_seconds"])


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(worker())
