module "network" {
  source          = "../../modules/network"
  environment     = "staging"
  region          = var.region
  subnet_cidr     = "10.10.0.0/24"
  allowed_ssh_ips = ["35.200.231.50"]
}
