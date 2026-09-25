import sqlite3
from contextlib import closing
from models import Difficulty

class Database:
    """Thin wrapper around the SQLite city database.

    Opens a new connection for every query and closes it afterwards, so an
    instance holds no open resources and is cheap to keep around.
 
    Args:
        db_path: Path to the ``terra.sqlite`` file.
    """
    def __init__(self, db_path : str):
        self.db_path : str = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_random_cities(self, difficulty : Difficulty, amount: int = 10,) -> list[tuple[str, str, float, float]]:
        """Pick random cities that match a difficulty.
 
        Args:
            difficulty: Defines the region and the minimum population.
            amount: Maximum number of cities to return.
 
        Returns:
            Up to ``amount`` rows of ``(ONR, name, latitude, longitude)`` in
            random order. Fewer rows are returned if not enough cities match.
        """

        # closes the connection no matter the outcome
        with closing(self._get_connection()) as connection:
            cursor = connection.cursor()

            query = """
                SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                FROM ort, land, kontinent
                WHERE land.KNR = kontinent.KNR 
                AND ort.LNR = land.LNR
                AND ort.Einwohner > :min_population
                AND (:country IS NULL OR land.Name = :country)
                AND (:continent IS NULL OR kontinent.Name = :continent)
                ORDER BY RANDOM()
                LIMIT :amount
            """

            cursor.execute(query, {
                "min_population": difficulty.settings.min_population,
                "country": difficulty.settings.region.country,
                "continent": difficulty.settings.region.continent,
                "amount": amount
            })

            return cursor.fetchall()
