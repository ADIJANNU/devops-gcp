INSERT INTO companies (name) VALUES ('Acme Logistics (staging)');

INSERT INTO equipment (company_id, equipment_code, name)
SELECT 1, 'STG-' || lpad(i::text, 4, '0'), 'Forklift ' || i
FROM generate_series(1, 12) AS i;
