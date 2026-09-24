terraform {
  backend "gcs" {
    bucket = "devops-learning-505512-fleetpulse-production-tfstate"
    prefix = "production/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
