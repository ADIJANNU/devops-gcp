import os
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
TOKEN_HOURS = 2

app = FastAPI(title="FleetPulse API")
bearer = HTTPBearer(auto_error=False)
# Used when the email doesn't exist, so response time doesn't reveal valid emails.
DUMMY_HASH = bcrypt.hashpw(b"dummy", bcrypt.gensalt(12))


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


class LoginRequest(BaseModel):
    email: str
    password: str


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    if creds is None:
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        # algorithms is pinned on purpose: never let the token choose its own.
        return jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="invalid or expired token")


def tenant_user(user=Depends(current_user)):
    if user.get("company_id") is None:
        raise HTTPException(status_code=403, detail="no company data for this role")
    return user


def platform_admin(user=Depends(current_user)):
    if user.get("role") != "platform_admin":
        raise HTTPException(status_code=403, detail="admin only")
    return user


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


def latest_equipment(company_id):
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(LATEST_SQL, (company_id,))
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


@app.post("/api/login")
def login(body: LoginRequest):
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id, company_id, password_hash, role FROM users WHERE email = %s",
            (body.email.strip().lower(),),
        )
        user = cur.fetchone()
    stored = user["password_hash"].encode() if user else DUMMY_HASH
    password_ok = bcrypt.checkpw(body.password.encode(), stored)
    if user is None or not password_ok:
        raise HTTPException(status_code=401, detail="invalid credentials")
    claims = {
        "sub": str(user["id"]),
        "company_id": user["company_id"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_HOURS),
    }
    return {
        "access_token": jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM),
        "token_type": "bearer",
    }


@app.get("/api/equipment")
def list_equipment(user=Depends(tenant_user)):
    return latest_equipment(user["company_id"])


@app.get("/api/summary")
def summary(user=Depends(tenant_user)):
    rows = latest_equipment(user["company_id"])
    counts = {"charging": 0, "in_use": 0, "idle": 0, "no_data": 0}
    for row in rows:
        counts[row["status"] or "no_data"] += 1
    return {
        "total": len(rows),
        **counts,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/equipment/{code}/history")
def history(code: str, hours: int = Query(24, ge=1, le=720), user=Depends(tenant_user)):
    company_id = user["company_id"]
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT id FROM equipment WHERE equipment_code = %s AND company_id = %s",
            (code, company_id),
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
            (code, company_id, hours),
        )
        return cur.fetchall()


@app.get("/api/admin/companies")
def admin_companies(user=Depends(platform_admin)):
    with db() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT c.id, c.name, count(e.id) AS equipment_count "
            "FROM companies c LEFT JOIN equipment e ON e.company_id = c.id "
            "GROUP BY c.id ORDER BY c.id"
        )
        return cur.fetchall()
