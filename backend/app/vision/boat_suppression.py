from __future__ import annotations


def keep_car(det: dict, horizon_y: int, aspect_ratio_range: tuple[float, float], area_range: tuple[float, float]) -> bool:
    x1, y1, x2, y2 = det["bbox"]
    w, h = max(1, x2 - x1), max(1, y2 - y1)
    cx, cy = x1 + w / 2, y1 + h / 2
    area = w * h
    ar = w / h
    if cy < horizon_y:
        return False
    if ar < aspect_ratio_range[0] or ar > aspect_ratio_range[1]:
        return False
    if area < area_range[0] or area > area_range[1]:
        return False
    return det.get("center_in_roi", True)
