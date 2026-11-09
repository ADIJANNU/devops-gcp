## Incident: first automated deploy failed its smoke test and rolled back

- **What happened:** The first `deploy-staging` run authenticated, connected to the cluster and applied the manifests, then the smoke test printed 000 for every check (curl never connected). The pipeline's rollback step then restored the previous API and dashboard images.
- **Impact:** None. The old Pods kept serving, and the rollback returned the cluster to the previous revision.
- **Detection:** The pipeline itself. The failed check turned the run red.
- **Root cause (most likely):** The smoke test reaches the API through a temporary `kubectl port-forward` and waited a fixed 3 seconds, which was not enough for the tunnel on a fresh runner. The script also discarded the tunnel's error output, so the log could not confirm this. The fix below worked, which is consistent with the timing explanation.
- **Fix:** The script now polls the tunnel for up to 30 seconds and prints the tunnel's own output if it never opens.
- **What worked:** Least-privilege deploy identity (apply and rollout worked), automatic rollback, and the rolling update keeping old Pods serving.
- **Gaps:** The rollback covers the two Deployments only, not the ingestion CronJob. The smoke test runs without login in CI. Silent failure (output hidden) made diagnosis slower, so scripts should surface errors.
