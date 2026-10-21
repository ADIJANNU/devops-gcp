#!/bin/bash
echo "Context: $(kubectl config current-context)"
echo ""
echo "=== Workloads ==="
kubectl get deploy,sts,cronjob
echo ""
echo "=== Pods ==="
kubectl get pods
echo ""
echo "=== Storage ==="
kubectl get pvc
