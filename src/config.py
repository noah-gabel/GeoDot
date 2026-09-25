"""Application wide configuration.

Holds absolute file paths, the map tile API key loaded from ``.env``, scoring constants and the UI theme (colors, fonts and sizes).
"""

import os
import sys

from dotenv import load_dotenv


# paths
def get_absolute_path(relative: str) -> str:
    """Get the absolute path to a path relative to teh project root.

    Works both when running with uv or in exe mode, where bundled files are extracted to the temporary ``sys._MEIPASS`` directory.

    Args:
        relative: Path relative to the project root, e.g. ``"terra.sqlite"``.

    Returns:
        The absolute path to the file or directory.
    """

    # __file__ stores the path to the current file which executes. In this case config.py
    # use os.path.dirname two times to move out of src into the main directory
    base_fallback = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # _MEIPASS is added by pyinstaller once run in exe mode
    # base_fallback is the fallback if the _MEIPASS attribute doesn't exist
    # for example when run with the normal uv run src/main.py command
    base = getattr(sys, "_MEIPASS", base_fallback)

    return os.path.join(base, relative)


ICON_DIR = get_absolute_path("./src/icon")
DATABASE_PATH = get_absolute_path("./terra.sqlite")

# API KEY
load_dotenv(get_absolute_path(".env"))
API_KEY = os.getenv("API_KEY")

# calculation config
EARTH_RADIUS = 6371.0
GUESS_TOLERANCE_KM = 5

# default settings
MAX_ROUND_SCORE = 5000
COUNTDOWN_TIME = (
    5  # sets the time in seconds which the countdown uses until the next round starts
)

# General UI
FG_COLOR = "#1e1e2e"
HEADING_TEXT_COLOR = "#5AB1FC"
FONT = "Segoe UI"
DISABLED_BUTTON_FG_COLOR = "#737273"
BUTTON_FG_COLOR = "#dd2476"
BUTTON_HOVER_FG_COLOR = "#ff4e9d"
RESULT_ENTRY_BAR_HEIGHT = 60

# start screen
INTRO_HEADING_ACCENT_COLOR = "#dd2476"
TEXT_COLOR = "#ffffff"
TEXT_DIM_COLOR = "#9494ab"
TEXT_FAINT_COLOR = "#6f6f88"

START_BUTTON_DISABLED_FG_COLOR = DISABLED_BUTTON_FG_COLOR
START_BUTTON_HOVER_FG_COLOR = BUTTON_HOVER_FG_COLOR
START_BUTTON_FG_COLOR = BUTTON_FG_COLOR

# Difficulty Cards
CARD_FG_COLOR = "#262636"
CARD_HOVER_FG_COLOR = "#2c2c3e"
CARD_BORDER_COLOR = "#33334a"
CARD_SELECT_BORDER_COLOR = "#dd2476"
CARD_WIDTH = 200
CARD_HEIGHT = 200
CARD_INNER_PADX = 16

GERMANY_DIFFICULTY_COLOR = "#5AB1FC"
EUROPE_DIFFICULTY_COLOR = "#FFC53D"
WORLDWIDE_DIFFICULTY_COLOR = "#dd2476"
UNSELECTED_DIFFICULTY_COLOR = "#737273"

# Guess Button
GUESS_BUTTON_FG_COLOR = BUTTON_FG_COLOR
GUESS_BUTTON_HOVER_FG_COLOR = BUTTON_HOVER_FG_COLOR
GUESS_BUTTON_DISABLED_FG_COLOR = DISABLED_BUTTON_FG_COLOR

# Map
TOLERANCE_RADIUS_PX = 6
BLOCKED_BINDING_SEQUENCES = (
    "<ButtonPress-1>",
    "<ButtonRelease-1>",
    "<B1-Motion>",
    "<Double-Button-1>",
    "<ButtonPress-2>",
    "<ButtonRelease-2>",
    "<B2-Motion>",
    "<ButtonPress-3>",
    "<ButtonRelease-3>",
    "<B3-Motion>",
    "<MouseWheel>",
    "<KeyPress>",
)
GUESS_MARKER_COLOR = "#dd2476"
GUESS_MARKER_CIRCLE_COLOR = "#8f0f45"

CITY_MARKER_COLOR_INSIDE = "#8a5a00"
CITY_MARKER_COLOR_OUTSIDE = "#FFC53D"

MARKER_TEXT_COLOR = "#1e1e2e"
RESULT_PATH_COLOR = "#6C6C8A"
RESULT_PATH_WIDTH = 3
