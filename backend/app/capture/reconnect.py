from __future__ import annotations


def next_backoff(current: int, maximum: int) -> int:
    if current <= 0:
        return 1
    return min(current * 2, maximum)
