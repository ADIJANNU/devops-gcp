import os
from contextlib import contextmanager
from datetime import datetime, timezone

import psycopg2
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

# TEMPORARY PLACEHOLDER: replaced by the company_id inside the login token
# when we build authentication. Never accept this from the request itself.
COMPANY_ID = int(os.environ["COMPANY_ID"])

app = FastAPI(title="FleetPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@contextmanager
def db():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASSWORD, connect_timeout=3,
    )
    try:
        yield conn
    finally:
        conn.close()


LATEST_SQL = """
SELECT e.equipment_code AS id, e.name,
       r.status, r.soc, r.temperature, r.recorded_at
FROM equipment e
LEFT JOIN LATERAL (
    SELECT status, soc, temperature, recorded_at
    FROM readings
    WHERE equipment_id = e.id
    ORDER BY recorded_at DESC
    LIMIT 1
) r ON true
WHERE e.company_id = %s
ORDER BY e.equipment_code
"""


def latest_equipment():
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(LATEST_SQL, (COMPANY_ID,))
        return cur.fetchall()


@app.get("/")
def root():
    return {"message": "FleetPulse API is running"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        with db() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ready"}


@app.get("/equipment")
def list_equipment():
    return latest_equipment()


@app.get("/summary")
def summary():
    rows = latest_equipment()
    counts = {"charging": 0, "in_use": 0, "idle": 0, "no_data": 0}
    for row in rows:
        counts[row["status"] or "no_data"] += 1
    return {
        "total": len(rows),
        **counts,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/equipment/{code}/history")
def history(code: str, hours: int = Query(24, ge=1, le=720)):
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id FROM equipment WHERE equipment_code = %s AND company_id = %s",
            (code, COMPANY_ID),
        )
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="equipment not found")
        cur.execute(
            """
            SELECT r.recorded_at, r.soc, r.temperature, r.status
            FROM readings r
            JOIN equipment e ON e.id = r.equipment_id
            WHERE e.equipment_code = %s AND e.company_id = %s
              AND r.recorded_at > now() - make_interval(hours => %s)
            ORDER BY r.recorded_at DESC
            LIMIT 1000
            """,
            (code, COMPANY_ID, hours),
        )
        return cur.fetchall()
