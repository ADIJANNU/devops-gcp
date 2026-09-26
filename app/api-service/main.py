from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(title="FleetPulse API")

# Allow the dashboard (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local dev; we'll restrict this properly later
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simulated in-memory equipment data (real DB comes later) ---
equipment = [
    {"id": "FBP-1174", "name": "Forklift A1", "status": "charging", "soc": 42},
    {"id": "FBP-1175", "name": "Forklift A2", "status": "in_use", "soc": 88},
    {"id": "FBP-1176", "name": "AGV B1", "status": "idle", "soc": 95},
    {"id": "FBP-1177", "name": "AGV B2", "status": "in_use", "soc": 61},
]

@app.get("/")
def root():
    return {"message": "FleetPulse API is running"}

@app.get("/equipment")
def list_equipment():
    return equipment

@app.get("/summary")
def summary():
    total = len(equipment)
    charging = len([e for e in equipment if e["status"] == "charging"])
    in_use = len([e for e in equipment if e["status"] == "in_use"])
    idle = len([e for e in equipment if e["status"] == "idle"])
    return {
        "total": total,
        "charging": charging,
        "in_use": in_use,
        "idle": idle,
        "timestamp": datetime.utcnow().isoformat()
    }
