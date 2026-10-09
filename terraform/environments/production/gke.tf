resource "google_container_cluster" "primary" {
  name     = "fleetpulse-production-cluster"
  location = var.region

  network    = module.network.vpc_id
  subnetwork = module.network.subnet_id

  enable_autopilot = true

  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "10.21.0.0/20"
    services_ipv4_cidr_block = "10.22.0.0/22"
  }

  deletion_protection = true
}
