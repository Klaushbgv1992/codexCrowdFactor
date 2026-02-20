import numpy as np

from app.vision.detector import Detector


def test_detector_runs():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    out = Detector().detect(frame, {})
    assert "person_count" in out and "car_count" in out
