from config import MAX_ROUND_SCORE, WORLDWIDE_DIFFICULTY_COLOR, EUROPE_DIFFICULTY_COLOR, GERMANY_DIFFICULTY_COLOR

def score_color(score: int) -> str:
    if score <= 1/3 * MAX_ROUND_SCORE:
        return WORLDWIDE_DIFFICULTY_COLOR
    elif score <= 2/3 * MAX_ROUND_SCORE:
        return EUROPE_DIFFICULTY_COLOR
    return GERMANY_DIFFICULTY_COLOR

def format_distance(distance_km: float) -> str:
    if distance_km < 1:
        return f"{distance_km * 1000:.0f} m"
    elif distance_km < 100:
        return f"{distance_km:.1f} km"
    return f"{distance_km:.0f} km"