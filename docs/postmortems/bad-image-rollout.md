## Trial: rollout with a nonexistent image tag

- **What I did:** Pointed the live staging API Deployment at a tag that doesn't exist.
- **What happened:** The new Pod went to ErrImagePull and never became Ready. The two old Pods kept serving, and the health and 401 smoke checks passed throughout.
- **Why:** A rolling update only removes old Pods as new ones pass their readiness probe, so a bad image can't take the service down.
- **Detection:** `rollout status` timed out; `describe pod` showed the registry error.
- **Fix:** `kubectl rollout undo`. The previous ReplicaSet was kept, so recovery was immediate.
- **Prevention:** CI should verify the image exists and runs before deploy, and the pipeline should run the smoke test after deploy and undo automatically if it fails. Manual `set image` also causes drift from git, so deploys should go through the pipeline.
