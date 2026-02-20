from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import cv2
import numpy as np


@dataclass
class StreamState:
    stream_connected: bool = False
    stream_status: str = "offline"
    last_frame_captured: Optional[str] = None
    last_error: Optional[str] = None


class YouTubeFrameCapture:
    def __init__(self, youtube_url: str, refresh_interval: int = 1800) -> None:
        self.youtube_url = youtube_url
        self.refresh_interval = refresh_interval
        self.stream_url: Optional[str] = None
        self.last_refresh = 0.0

    def get_stream_url(self) -> str:
        result = subprocess.run(["yt-dlp", "-f", "best[height<=720]", "-g", self.youtube_url], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise ConnectionError(result.stderr.strip() or "yt-dlp failed")
        return result.stdout.strip().splitlines()[0]

    def ensure_stream_url(self) -> str:
        now = time.time()
        if not self.stream_url or now - self.last_refresh > self.refresh_interval:
            self.stream_url = self.get_stream_url()
            self.last_refresh = now
        return self.stream_url

    def capture_frame(self) -> np.ndarray:
        url = self.ensure_stream_url()
        cap = cv2.VideoCapture(url)
        ok, frame = cap.read()
        cap.release()
        if not ok:
            self.stream_url = None
            raise ConnectionError("Failed to capture frame")
        return frame


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
