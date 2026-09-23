## Incident: Manual firewall deletion causing drift

- **What broke:** allow-ssh firewall rule deleted manually via gcloud CLI (simulating an out-of-band console/manual change)
- **Why:** Simulated a common real-world cause of infra drift — someone bypassing IaC and changing infra directly
- **Impact:** SSH access (port 22) to devops-vm would be blocked
- **Detection:** terraform plan flagged the missing firewall rule as needing recreation
- **Fix:** terraform apply recreated the rule, restoring SSH access
- **Prevention (real-world):** Restrict manual console/CLI access to production infra; enforce all changes through CI/CD pipeline; consider org policies blocking direct resource deletion
