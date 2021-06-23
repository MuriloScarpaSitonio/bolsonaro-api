variable "project_name" {
  description = "The name of the project."
  type        = string
}

variable "allocated_storage" {
  description = "The allocated storage in gibibytes."
  type        = number
}

variable "engine" {
  description = "The database engine to use."
  type        = string
}

variable "engine_version" {
  description = "The engine version to use."
  type        = string
}

variable "instance_class" {
  description = "The instance type of the RDS."
  type        = string
}

variable "name" {
  description = "The name of the database to create when the DB instance is created."
  type        = string
}

variable "username" {
  description = "Username for the master DB user."
  type        = string
}

variable "port" {
  description = "The database port."
  type        = number
}

variable "password" { # SSM
  description = "The database password for the master user"
  type        = string
  sensitive   = true
}

variable "parameter_group_family" {
  description = "The family of the DB parameter group."
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the security."
  type        = string
}

variable "vpc_cidr_blocks" {
  description = "List of CIDR blocks for the security group."
  type        = list(string)

  validation {
    condition     = length(var.vpc_cidr_blocks) > 0
    error_message = "VPC CIDR Blocks must have at least one value."
  }
}

variable "subnet_ids" {
  description = "A list of VPC subnet IDs."
  type        = list(string)

  validation {
    # length(var.subnet_ids) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.subnet_ids) > 1 && length(var.subnet_ids) < 3
    error_message = "Must be a list of two values because we have two subnets for the RDS."
  }
}

variable "ecs_security_group_id" {
  description = "Security group ID to ensure that only traffic from ECS can talk to the database."
  type        = string
}