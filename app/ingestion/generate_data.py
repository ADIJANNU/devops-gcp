import random
from datetime import datetime

# Same equipment list as the API service, for now (real DB sync comes later)
equipment_ids = ["FBP-1174", "FBP-1175", "FBP-1176", "FBP-1177"]

def generate_reading(equipment_id):
    return {
        "equipment_id": equipment_id,
        "soc": random.randint(10, 100),          # State of Charge %
        "temperature": round(random.uniform(20, 45), 1),
        "status": random.choice(["charging", "in_use", "idle"]),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    for eq_id in equipment_ids:
        reading = generate_reading(eq_id)
        print(reading)
