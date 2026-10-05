output "vpc_name" {
  value = module.network.vpc_name
}

output "subnet_name" {
  value = module.network.subnet_name
}

output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  value     = google_container_cluster.primary.endpoint
  sensitive = true
}
