## Trial: container exceeds its memory limit

- **What I did:** Ran a throwaway Pod that allocates 300 MB with a 128 Mi memory limit.
- **What happened:** The container was killed (OOMKilled, exit code 137 = 128 + SIGKILL), then restarted repeatedly and entered CrashLoopBackOff.
- **Detection:** `kubectl describe pod` showed Last State: Terminated, Reason: OOMKilled. The logs were empty because the process died before printing anything, so the Pod status is the evidence, not the logs.
- **Fix:** Raised the memory limit to 512 Mi. The Pod completed normally.
- **Prevention:** Set limits from measured usage (`kubectl top pod`), alert on restart counts and OOMKilled, and investigate leaks instead of only raising limits. CPU limits throttle, memory limits kill, which is why they behave differently.
