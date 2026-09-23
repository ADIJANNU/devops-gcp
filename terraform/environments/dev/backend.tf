terraform {
  backend "gcs" {
    bucket = "devops-learning-505512-tfstate"
    prefix = "dev/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}
