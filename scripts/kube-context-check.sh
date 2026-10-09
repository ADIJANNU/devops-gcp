#!/bin/bash

CTX=$(kubectl config current-context)
echo "Current context: $CTX"

if [[  "$CTX" == gke_* ]];then
	echo "You are on a REAL GKE cluster. Be careful with delete and scale."
elif [[  "$CTX" == kind_*  ]];then
	echo "You are on the local kind cluster. Safe to experiment."
else
	echo "Unknown context..."
fi


