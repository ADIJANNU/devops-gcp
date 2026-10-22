#!/bin/bash
# Smoke test for the FleetPulse API through a temporary port-forward.
# Exits 0 if every check passes, 1 if any fails.

PORT=8000
FAILED=0

kubectl port-forward svc/fleetpulse-api ${PORT}:8000 >/dev/null 2>&1 &
PF_PID=$!
trap 'kill $PF_PID 2>/dev/null' EXIT

sleep 3

check() {
  local path=$1
  local expected=$2
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" "localhost:${PORT}${path}")
  if [[ "$code" == "$expected" ]]; then
    echo "[PASS] $path -> $code"
  else
    echo "[FAIL] $path -> $code (expected $expected)"
    FAILED=1
  fi
}

check /healthz 200
check /readyz 200
check /api/summary 200
check /api/equipment 200
check /api/equipment/NOPE/history 404

if [[ $FAILED -eq 0 ]]; then
  echo "All checks passed"
else
  echo "Some checks failed"
fi
exit $FAILED
