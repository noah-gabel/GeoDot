# GeoDot

A little GeoGuessr-inspired game — except instead of dropping you into Street View, GeoDot just tells you a **city name**, and you have to click on the map where you think it is.

This started as a fun side project for a school class, so don't expect production-grade polish everywhere, but it works, it's fun to play, and it was a great learning experience. If you stumbled on this from outside class: hey, welcome, feel free to poke around!

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [License](#license)

## Features

- 5 difficulty levels, from "major German cities" to "literally anywhere on Earth"
- Click-to-guess map interaction
- A little animated score reveal after each round
- End-of-game recap map showing every guess vs. the real answer, with clickable rounds

## Tech Stack

- **Python 3.12+**
- **[customtkinter](https://github.com/TomSchimansky/CustomTkinter)** for the UI
- **[tkintermapview](https://github.com/TomSchimansky/TkinterMapView)** for the interactive map
- **SQLite** for the city database (bundled `terra.sqlite`, sourced from [inf-schule](https://www.inf-schule.de/) for learning purposes)
- **[uv](https://docs.astral.sh/uv/)** for dependency management

## Getting Started

### You'll need

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A free CARTO API key for the map tiles (see below)

### Install

```bash
git clone <your-repo-url>
cd geodot
uv sync
```

### Set up your `.env`

GeoDot uses CARTO's map tiles, which are free to use but require an API key (no CARTO account needed).

1. Grab a free key at [carto.com/basemaps/apikey](https://carto.com/basemaps/apikey). takes about a minute
2. Create a `.env` file in the project root:

   ```env
   API_KEY=your_carto_api_key_here
   ```

Grab your own key rather than reusing someone else's.

### Run it

```bash
uv run src/main.py
```

Pick a difficulty, hit start, click where you think the city is and click the guess button (or hit **Space** to submit), and see how close you got. Repeat until the round count runs out, then check your total score.

## Project Structure

```
geodot/
├── src/
│   ├── main.py              # entry point
│   ├── app.py                # main window / screen switching
│   ├── config.py             # colors, fonts, tuning values, API key loading
│   ├── database.py           # pulls random cities by difficulty from SQLite
│   ├── game_manager.py       # the actual game state machine
│   ├── models.py             # Coordinates, City, Guess, Difficulty, etc.
│   ├── score.py               # haversine distance + scoring formula
│   └── ui/
│       ├── screen.py          # base class for switchable screens
│       ├── start.py           # menu / difficulty picker
│       ├── game.py            # gameplay screen
│       ├── result.py          # end screen
│       ├── map_controller.py  # all the map click/marker logic
│       └── formatting.py      # small display helpers
├── pyproject.toml
├── uv.lock
└── LICENSE
```

## How It Works

### Difficulty levels

| Difficulty | Where the cities are from | Population cutoff | How forgiving the scoring is |
|---|---|---|---|
| Easy | Germany | 100k+ | Strict |
| Standard | Germany | 50k+ | Strict |
| Hard | Europe | 200k+ | Medium |
| Extreme | Europe | 100k+ | Medium |
| Impossible | Anywhere in the world | 300k+ | Loose |

### Scoring

Distance between your guess and the real city is worked out with the **Haversine formula** (accounts for the Earth being round, not flat). That distance then feeds into:

```
score = 5000 × e^(−max(distance − 5km, 0) / decay)
```

Guess within 5 km and you get the full 5,000 points. Beyond that, points fall off exponentially — how fast depends on the difficulty's decay value from the table above.

## License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for the full text.
