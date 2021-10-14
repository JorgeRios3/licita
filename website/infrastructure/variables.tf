# core

variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-west-2"
}

# networking

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

# load balancer

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/ping/"
}

# logs

variable "log_retention_in_days" {
  default = 30
}

# key pair

variable "ssh_pubkey_file" {
  description = "Path to an SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}

# ecs

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "production"
}
variable "amis" {
  description = "Which AMI to spawn."
  default = {
    us-west-2 = "ami-06cb61a83c506fe88"
  }
}
variable "instance_type" {
  default = "t2.micro"
}
variable "docker_image_url_django" {
  description = "Docker image to run in the ECS cluster"
  default     = "744313738431.dkr.ecr.us-west-2.amazonaws.com/djangoapp:1008v4"

}
variable "docker_image_url_nginx" {
  description = "Docker image to run in the ECS cluster"
  default     = "744313738431.dkr.ecr.us-west-2.amazonaws.com/nginx:1005"

}
variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 1
}
variable "root_block_size" {
  default = 10
}

# auto scaling

variable "autoscale_min" {
  description = "Minimum autoscale (number of EC2)"
  default     = "2"
}
variable "autoscale_max" {
  description = "Maximum autoscale (number of EC2)"
  default     = "3"
}
variable "autoscale_desired" {
  description = "Desired autoscale (number of EC2)"
  default     = "2"
}

# rds

variable "rds_db_name" {
  description = "RDS database name"
  default     = "mydb"
}
variable "rds_username" {
  description = "RDS database username"
  default     = "principal"
}
variable "rds_password" {
  description = "RDS database password"
  default     = "kB!WuXFkvwaWJ2t3"
}
variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t2.micro"
}

# domain

variable "certificate_arn" {
  description = "AWS Certificate Manager ARN for validated domain"
  default     = "arn:aws:acm:us-west-2:744313738431:certificate/ac23c1e6-c109-4b91-af29-27d345f4a69b"
}
