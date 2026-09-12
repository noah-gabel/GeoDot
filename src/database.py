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

            match difficulty:
                case Difficulty.EASY:
                    source = "FROM land, ort"
                    filters = "ort.LNR = land.LNR AND land.Name = 'Deutschland' AND ort.Einwohner > 100000"
                case Difficulty.STANDARD:
                        source = "FROM land, ort"
                        filters = "ort.LNR = land.LNR AND land.Name = 'Deutschland' AND ort.Einwohner > 50000"
                case Difficulty.HARD:
                    source = "FROM ort, land, kontinent"
                    filters = "ort.LNR = land.LNR AND land.KNR = kontinent.KNR AND kontinent.Name = 'Europa' AND ort.Einwohner > 200000"
                case Difficulty.EXTREME:
                    source = "FROM ort, land, kontinent"
                    filters = "ort.LNR = land.LNR AND land.KNR = kontinent.KNR AND kontinent.Name = 'Europa' AND ort.Einwohner > 100000"
                case Difficulty.IMPOSSIBLE:
                    source = "FROM ort"
                    filters = "ort.Einwohner > 300000"
                case _:
                    raise ValueError(f'Unknown difficulty: {difficulty}')

            query = f"""
                SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                {source}
                WHERE {filters}
                ORDER BY RANDOM()
                LIMIT ?
            """

            cursor.execute(query, (amount, ))
            return cursor.fetchall()
