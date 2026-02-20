from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app.vision.boat_suppression import keep_car


class Detector:
    """Lightweight CV fallback detector (contours) to keep app runnable without heavy model runtime."""

    def detect(self, frame: np.ndarray, scene_cfg: dict[str, Any]) -> dict[str, int]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thr = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        person_count = 0
        car_count = 0
        horizon_y = scene_cfg.get("horizon_y", 350)
        ar_range = tuple(scene_cfg.get("car_filters", {}).get("aspect_ratio_range", [1.0, 4.0]))
        area_range = tuple(scene_cfg.get("car_filters", {}).get("area_range", [800, 25000]))

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            if area < 150:
                continue
            bbox = [x, y, x + w, y + h]
            if w > h:
                if keep_car({"bbox": bbox, "center_in_roi": True}, horizon_y, ar_range, area_range):
                    car_count += 1
            else:
                person_count += 1
        return {"person_count": person_count, "car_count": car_count}
