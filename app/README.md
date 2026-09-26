# FleetPulse App Services

- `api-service/` — FastAPI service serving equipment list and fleet summary stats
- `ingestion/` — Simulates equipment telemetry generation (will become a Kubernetes CronJob)
- `dashboard/` — Static HTML/JS dashboard calling the API service

## Running locally (Day 2 stage — no Docker/K8s yet)
cd api-service
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
