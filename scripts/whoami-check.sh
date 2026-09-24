#!/bin/bash

echo "Active GCP account: $(gcloud config get-value account)"
echo "Active project: $(gcloud config get-value project)"
echo "Active region/zone: $(gcloud config get-value compute/region) / $(gcloud config get-value compute/zone)"


