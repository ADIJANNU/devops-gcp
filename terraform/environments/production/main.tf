module "network" {
  source          = "../../modules/network"
  environment     = "production"
  region          = var.region
  subnet_cidr     = "10.20.0.0/24"
  allowed_ssh_ips = ["35.200.231.50/32"]
}
