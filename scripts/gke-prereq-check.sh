#!/bin/bash

echo "=== Checking required APIs for GKE ==="
REQUIRED_APIS=("container.googleapis.com" "compute.googleapis.com")

for api in "${REQUIRED_APIS[@]}"; do
  status=$(gcloud services list --enabled --filter="name:$api" --format="value(name)")
  if [[ -n "$status" ]]; then
    echo "[OK] $api is enabled"
  else
    echo "[MISSING] $api is NOT enabled"
  fi
done
