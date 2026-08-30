import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

EARTH_RADIUS = 6371.0
GUESS_TOLERANCE_KM = 0.025


FG_COLOR="#1e1e2e"