## Incident: Cloud Armor allowlist blocked the legitimate client

- **What happened:** After attaching the allowlist, the VM was correctly blocked (403), but my own laptop browser was also blocked.
- **Root cause:** The allow rule contained 192.168.0.244/32, my laptop's private LAN address (copied from the local network settings). The load balancer only ever sees public egress addresses, so the rule could never match.
- **Detection:** Rule contents compared with the public IP from `curl -4 ifconfig.me` (106.51.111.236). Load balancer logs showed which source IPs were being denied.
- **Fix:** Updated rule 1000 to the public IPv4 address. Verified both cases: laptop allowed, phone on mobile data blocked (403), VM blocked (403).
- **Lesson:** Allowlist public egress addresses, never private (RFC 1918) ranges. Home IPs also change, so real clients should come through a stable VPN egress IP.
- **Open item:** The deny logs also showed 156.225.1.33 and 103.218.241.30, which I did not identify and did not allow.
