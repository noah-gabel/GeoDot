from models import Coordinates, Difficulty
from score import haversine_distance, calculate_score
from database import Database

berlin = Coordinates(52.520008, 13.404954)
munich = Coordinates(48.135125, 11.581981)

distance = haversine_distance(berlin, munich)
score = calculate_score(distance_km=distance, difficulty=Difficulty.EASY)

#print(f"Die Luftlinie zwischen Berlin und München beträgt: {distance:.2f} km")
#print(f"Der score beträgt: {score}")

db = Database("./terra.sqlite")
from collections import Counter
print(Counter(db.get_random_cities(Difficulty.EASY, amount=1)[0][1] for _ in range(20)))