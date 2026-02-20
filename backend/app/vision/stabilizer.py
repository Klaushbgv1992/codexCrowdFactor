from __future__ import annotations

from collections import deque
from statistics import median


class CountStabilizer:
    def __init__(self, window_seconds: int = 180):
        self.window = window_seconds
        self.readings: dict[str, deque[tuple[int, int]]] = {}

    def add_reading(self, zone: str, timestamp: int, count: int) -> None:
        if zone not in self.readings:
            self.readings[zone] = deque()
        self.readings[zone].append((timestamp, count))
        cutoff = timestamp - self.window
        while self.readings[zone] and self.readings[zone][0][0] < cutoff:
            self.readings[zone].popleft()

    def get_stable_count(self, zone: str) -> int:
        if zone not in self.readings or not self.readings[zone]:
            return 0
        return int(median(c for _, c in self.readings[zone]))
