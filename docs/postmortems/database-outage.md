## Trial: database outage

- **What I did:** Scaled the Postgres StatefulSet to 0 replicas on staging.
- **What happened:** The API's /readyz (which runs SELECT 1) started failing, so both API Pods became NotReady and left the Service endpoints. Restart count stayed at 0 because /healthz does not touch the database, so liveness kept passing. Ingestion runs failed for the duration.
- **Impact:** API requests failed while there were no healthy backends. Readings were not recorded for the outage window, leaving a permanent gap in the history.
- **Detection:** `kubectl get pods` (0/1, 0 restarts), `kubectl get endpoints` (empty), readiness probe failure events.
- **Recovery:** Scaled Postgres back to 1. The PVC reattached, data intact, and the API Pods became Ready on their own without restarts.
- **Why the probe split matters:** If liveness depended on the database, a database outage would make Kubernetes restart every API Pod in a loop, adding load and hiding the real cause.
- **Prevention:** Alert on API Pods NotReady and on failed Ingestion jobs, back up the database, and decide whether Ingestion should buffer or back-fill after an outage. A single Postgres replica is a known single point of failure.
