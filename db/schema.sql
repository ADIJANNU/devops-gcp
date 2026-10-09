CREATE TABLE companies (
  id          serial PRIMARY KEY,
  name        text NOT NULL UNIQUE,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE equipment (
  id             serial PRIMARY KEY,
  company_id     int NOT NULL REFERENCES companies(id),
  equipment_code text NOT NULL UNIQUE,
  name           text NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE readings (
  id           bigserial PRIMARY KEY,
  equipment_id int NOT NULL REFERENCES equipment(id),
  soc          smallint NOT NULL CHECK (soc BETWEEN 0 AND 100),
  temperature  numeric(4,1) NOT NULL,
  status       text NOT NULL CHECK (status IN ('charging', 'in_use', 'idle')),
  recorded_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id            serial PRIMARY KEY,
  company_id    int REFERENCES companies(id),
  email         text NOT NULL UNIQUE,
  password_hash text NOT NULL,
  role          text NOT NULL CHECK (role IN ('client_viewer', 'client_admin', 'platform_admin')),
  created_at    timestamptz NOT NULL DEFAULT now(),
  CHECK ((role = 'platform_admin') = (company_id IS NULL))
);

CREATE INDEX idx_equipment_company ON equipment (company_id);
CREATE INDEX idx_readings_equipment_time ON readings (equipment_id, recorded_at DESC);
