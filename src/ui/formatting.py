"""Helpers that turn raw values into display text and colors."""

from config import MAX_ROUND_SCORE, WORLDWIDE_DIFFICULTY_COLOR, EUROPE_DIFFICULTY_COLOR, GERMANY_DIFFICULTY_COLOR

def score_color(score: int) -> str:
    """Return the display color for a round score.

    Scores in the lowest third of ``MAX_ROUND_SCORE`` are pink, the middle third yellow and the top third blue.
    """
    if score <= 1/3 * MAX_ROUND_SCORE:
        return WORLDWIDE_DIFFICULTY_COLOR
    elif score <= 2/3 * MAX_ROUND_SCORE:
        return EUROPE_DIFFICULTY_COLOR
    return GERMANY_DIFFICULTY_COLOR

def format_distance(distance_km: float) -> str:
    """Format a distance with a suitable unit and precision.

    Examples:
        ``0.35`` becomes ``"350 m"``, ``12.345`` becomes ``"12.3 km"`` and ``812.6`` becomes ``"813 km"``.
    """
    if distance_km < 1:
        return f"{distance_km * 1000:.0f} m"
    elif distance_km < 100:
        return f"{distance_km:.1f} km"
    return f"{distance_km:.0f} km"