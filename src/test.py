from models import Coordinates, Difficulty
from score import haversine_distance, calculate_score


berlin = Coordinates(52.520008, 13.404954)
munich = Coordinates(48.135125, 11.581981)

distance = haversine_distance(berlin, munich)
score = calculate_score(distance_km=distance, difficulty=Difficulty.EASY)

print(f"Die Luftlinie zwischen Berlin und München beträgt: {distance:.2f} km")
print(f"Der score beträgt: {score}")