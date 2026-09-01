import os
from dotenv import load_dotenv

# API KEY
load_dotenv()
API_KEY = os.getenv("API_KEY")

# calculation config
EARTH_RADIUS = 6371.0
GUESS_TOLERANCE_KM = 0.025

#General UI
FG_COLOR="#1e1e2e"
HEADING_TEXT_COLOR = "#5AB1FC"
FONT = "Segoe UI"

# Guess Button
GUESS_BUTTON_FG_COLOR = "#dd2476"
GUESS_BUTTON_HOVER_FG_COLOR = "#ff4e9d"
GUESS_BUTTON_DISABLED_FG_COLOR = "#737273"

# Map
TOLERANCE_RADIUS_PX = 6
BLOCKED_BINDING_SEQUENCES = (
        "<ButtonPress-1>", "<ButtonRelease-1>", "<B1-Motion>", "<Double-Button-1>",
        "<ButtonPress-2>", "<ButtonRelease-2>", "<B2-Motion>",
        "<ButtonPress-3>", "<ButtonRelease-3>", "<B3-Motion>",
        "<MouseWheel>",
        "<KeyPress>",
    )
GUESS_MARKER_COLOR = "#dd2476"
GUESS_MARKER_CIRCLE_COLOR = "#8f0f45"

CITY_MARKER_COLOR_INSIDE="#8a5a00"
CITY_MARKER_COLOR_OUTSIDE="#FFC53D"

MARKER_TEXT_COLOR = "#1e1e2e"
RESULT_PATH_COLOR = "#6C6C8A"
RESULT_PATH_WIDTH = 3

