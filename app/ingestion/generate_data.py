import os
import random

import psycopg2

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    connect_timeout=5,
)

with conn, conn.cursor() as cur:
    cur.execute("SELECT id, equipment_code FROM equipment ORDER BY id")
    rows = cur.fetchall()
    for equipment_id, code in rows:
        cur.execute(
            "INSERT INTO readings (equipment_id, soc, temperature, status) "
            "VALUES (%s, %s, %s, %s)",
            (
                equipment_id,
                random.randint(10, 100),
                round(random.uniform(20, 45), 1),
                random.choice(["charging", "in_use", "idle"]),
            ),
        )
    print(f"inserted {len(rows)} readings")

conn.close()
