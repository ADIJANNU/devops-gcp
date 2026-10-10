#!/bin/bash

CTX=$(kubectl config current-context)
echo "Current context: $CTX"

if [[ "$CTX" == *production* ]]; then
	echo "!!! PRODUCTION CLUSTER. Double-check before any apply, delete or scale. !!!"
elif [[  "$CTX" == gke_* ]];then
	echo "Staging GKE cluster. Real resources, but not production."
elif [[  "$CTX" == kind_*  ]];then
	echo "You are on the local kind cluster. Safe to experiment."
else
	echo "Unknown context..."
fi


