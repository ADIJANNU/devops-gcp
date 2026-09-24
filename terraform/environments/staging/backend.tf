terraform {
  backend "gcs" {
    bucket = "devops-learning-505512-fleetpulse-staging-tfstate"
    prefix = "staging/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
