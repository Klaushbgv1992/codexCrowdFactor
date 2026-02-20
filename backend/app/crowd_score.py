from __future__ import annotations


def calculate_crowd_factor(parking_cars: int, pier_people: int, beach_people: int, water_people: int, config: dict) -> int:
    weights = config.get("crowd_weights", {"parking": 0.30, "pier": 0.15, "beach": 0.35, "water": 0.20})
    max_values = config.get("crowd_max_values", {"parking_cars": 50, "pier_people": 40, "beach_people": 80, "water_people": 25})
    scores = {
        "parking": min(parking_cars / max_values["parking_cars"], 1.0),
        "pier": min(pier_people / max_values["pier_people"], 1.0),
        "beach": min(beach_people / max_values["beach_people"], 1.0),
        "water": min(water_people / max_values["water_people"], 1.0),
    }
    return int(round(sum(scores[k] * weights[k] for k in weights) * 100))


def level_meta(score: int) -> tuple[str, str, str]:
    if score <= 15:
        return "empty", "#10B981", "Beach is empty — perfect for a private lesson!"
    if score <= 35:
        return "quiet", "#06B6D4", "Quiet morning at the beach. Great time to learn to surf!"
    if score <= 55:
        return "moderate", "#EAB308", "Good vibes at the beach today. Join a group lesson!"
    if score <= 75:
        return "busy", "#F97316", "Beach is lively! Book an early morning lesson tomorrow."
    return "packed", "#EF4444", "Beach is packed! Beat the crowds — book a sunrise session."
