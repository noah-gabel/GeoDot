import sqlite3
from contextlib import closing
from models import Difficulty


class Database:
    def __init__(self, db_path : str):
        self.db_path : str = db_path;

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_random_cities(self, difficulty : Difficulty, amount: int = 10,) -> list[tuple[str, str, float, float]]:
        # closes the connection no matter the outcome
        with closing(self._get_connection()) as connection:
            cursor = connection.cursor()

            match difficulty:
                case Difficulty.EASY:
                    query="""
                        SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                        FROM ort, land
                        WHERE ort.LNR = land.LNR
                        AND land.Name = 'Deutschland'
                        AND ort.Einwohner > 500000
                        ORDER BY RANDOM()
                        LIMIT ?
                    """
                case Difficulty.STANDARD:
                        query="""
                            SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                            FROM ort, land
                            WHERE ort.LNR = land.LNR
                            AND land.Name = 'Deutschland'
                            AND ort.Einwohner > 50000
                            ORDER BY RANDOM()
                            LIMIT ?
                        """
                case Difficulty.HARD:
                    query="""
                        SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                        FROM ort, land, kontinent
                        WHERE ort.Einwohner > 300000
                        AND ort.LNR = land.LNR
                        AND land.KNR = kontinent.KNR
                        AND kontinent.Name = 'Europa'
                        ORDER BY RANDOM()
                        LIMIT ?
                    """
                case Difficulty.EXTREME:
                    query= """
                        SELECT ort.ONR, ort.Name, ort.Breite, ort.Laenge
                        FROM ort, land, kontinent
                        WHERE ort.Einwohner > 100000
                        AND ort.LNR = land.LNR
                        AND land.KNR = kontinent.KNR
                        AND kontinent.Name = 'Europa'
                        ORDER BY RANDOM()
                        LIMIT ?
                    """
                case Difficulty.IMPOSSIBLE:
                    query = """
                        SELECT ONR, Name, Breite, Laenge
                        FROM ort
                        WHERE Einwohner > 200000
                        ORDER BY RANDOM()
                        LIMIT ?
                    """
                case _:
                    raise ValueError(f'Unknown difficulty: {difficulty}')

            cursor.execute(query, (amount, ))
            return cursor.fetchall()
