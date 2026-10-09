#!/bin/bash
echo "Context: $(kubectl config get-contexts)"
echo ""
echo "=== Workloads ==="
kubectl get deploy,sts,cronjob
echo ""
echo "=== Pods ==="
kubectl get pods
echo ""
echo "=== Storage ==="
kubectl get pvc
