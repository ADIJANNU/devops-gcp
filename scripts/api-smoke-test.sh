#!/bin/bash
# Usage: SMOKE_EMAIL=... SMOKE_PASSWORD=... ./api-smoke-test.sh
PORT=8000
FAILED=0

kubectl port-forward svc/fleetpulse-api ${PORT}:8000 >/dev/null 2>&1 &
PF_PID=$!
trap 'kill $PF_PID 2>/dev/null' EXIT
sleep 3

check() {  # usage: check PATH EXPECTED_CODE [TOKEN]
  local code
  if [[ -n "$3" ]]; then
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $3" "localhost:${PORT}$1")
  else
    code=$(curl -s -o /dev/null -w "%{http_code}" "localhost:${PORT}$1")
  fi
  if [[ "$code" == "$2" ]]; then
    echo "[PASS] $1 -> $code"
  else
    echo "[FAIL] $1 -> $code (expected $2)"
    FAILED=1
  fi
}

check /healthz 200
check /readyz 200
check /api/summary 401

if [[ -n "$SMOKE_EMAIL" && -n "$SMOKE_PASSWORD" ]]; then
  TOKEN=$(curl -s -X POST "localhost:${PORT}/api/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$SMOKE_EMAIL\",\"password\":\"$SMOKE_PASSWORD\"}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
  if [[ -z "$TOKEN" ]]; then
    echo "[FAIL] login returned no token"
    FAILED=1
  else
    echo "[PASS] login"
    check /api/summary 200 "$TOKEN"
    check /api/equipment 200 "$TOKEN"
    check /api/equipment/NOPE/history 404 "$TOKEN"
  fi
fi

[[ $FAILED -eq 0 ]] && echo "All checks passed" || echo "Some checks failed"
exit $FAILED
