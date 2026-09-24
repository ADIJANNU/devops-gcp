# Command Cheatsheet

## Auth
gcloud auth login                          -> for you running gcloud/gsutil commands
gcloud auth application-default login       -> for Terraform/SDKs calling GCP APIs

## Dev VM management
gcloud compute instances stop dev-workstation --zone=asia-south1-a
gcloud compute instances start dev-workstation --zone=asia-south1-a
gcloud compute ssh dev-workstation --zone=asia-south1-a

## Terraform state bucket
GCS state bucket: devops-learning-505512-tfstate

## FleetPulse Terraform state buckets
Staging:    devops-learning-505512-fleetpulse-staging-tfstate
Production: devops-learning-505512-fleetpulse-production-tfstate
