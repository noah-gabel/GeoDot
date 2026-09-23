import sqlite3
from contextlib import closing
from models import Difficulty

class Database:
    def __init__(self, db_path : str):
        self.db_path : str = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_random_cities(self, difficulty : Difficulty, amount: int = 10,) -> list[tuple[str, str, float, float]]:
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
