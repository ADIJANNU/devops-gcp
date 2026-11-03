# CI pipeline

**On pull request:** Gitleaks (history), pip-audit, Terraform scan (report only), build all three images, Trivy image scan. No GCP access.
**On merge to main:** same checks, then keyless login to GCP and push images tagged with the 7-character commit SHA.

## Identity
Workload Identity Federation. No service account key exists. Provider trusts only repo adijannu/devops-gcp on refs/heads/main. The CI service account can only push to one Artifact Registry repository.

## Known gaps
- Third-party actions are pinned to major tags, not commit SHAs.
- Terraform scan is report-only.
- Image tags are mutable in the registry (immutable tags could be enabled).
- Deployment is not automated yet.
- Trivy blocked the dashboard image: 3 CRITICAL findings (brotli-libs, libcrypto3, libssl3) in the nginx-unprivileged:1.27-alpine base, all with fixes available. A fresh `docker pull` did not help, because the tag's Alpine base was not rebuilt. Fixed with `apk upgrade` in the Dockerfile, then returned to the non-root user (uid 101) and verified the container serves. The OpenSSL CVE was 32-bit only, so likely not exploitable on our nodes, but fixed anyway. Trade-off: builds are no longer bit-for-bit reproducible.
