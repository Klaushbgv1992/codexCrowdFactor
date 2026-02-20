from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    stream_connected: bool
    last_frame_captured: str | None
    last_detection_run: str | None
    model_loaded: bool
    database_connected: bool
    uptime_seconds: int
