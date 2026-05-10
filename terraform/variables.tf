variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "varoq"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small" # 2 vCPU / 2GB RAM — fits api + bot + postgres comfortably
}

variable "ssh_public_key" {
  description = "Your SSH public key (~/.ssh/id_ed25519.pub)"
  type        = string
  sensitive   = true
}

variable "my_ip" {
  description = "Your IP for SSH access (run: curl ifconfig.me)"
  type        = string
}
