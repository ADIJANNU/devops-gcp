variable "environment" {
  description = "Environment name, e.g. staging or production"
  type        = string
}

variable "region" {
  type    = string
  default = "asia-south1"
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  type        = string
}

variable "allowed_ssh_ips" {
  description = "List of IPs allowed to SSH in (private access)"
  type        = list(string)
}
