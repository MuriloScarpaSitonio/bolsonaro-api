variable "project_name" {
  description = "The name of the project"
  type        = string
}


variable "cidr_block" {
  description = "VPC Classless Inter-Domain Routing block"
  type        = string
}


variable "routes_cidr_blocks" {
  description = "VPC routes that will be associated to the route table"
  type        = list(string)
  default     = ["0.0.0.0/0"]

  validation {
    condition     = length(var.routes_cidr_blocks) > 0
    error_message = "Must be a list with at least one route CIDR block."
  }
}


variable "public_cidr_blocks" {
  description = "Two public Classless Inter-Domain Routing block"
  type        = list(string)

  validation {
    # length(var.public_cidr_blocks) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.public_cidr_blocks) > 1 && length(var.public_cidr_blocks) < 3
    error_message = "Must be a list of two values because we have two public subnets."
  }
}

variable "private_cidr_blocks" {
  description = "Two private instance Classless Inter-Domain Routing block"
  type        = list(string)

  validation {
    # length(var.private_cidr_blocks) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.private_cidr_blocks) > 1 && length(var.private_cidr_blocks) < 3
    error_message = "Must be a list of two values because we have two private subnets."
  }
}


variable "availability_zones" {
  description = "Two availability zones"
  type        = list(string)

  validation {
    # length(var.availability_zones) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.availability_zones) > 1 && length(var.availability_zones) < 3
    error_message = "Must be a list of two values because we have one public zone and one private zone."
  }
}

variable "eip_private_ip_to_associate" {
  description = "Primary or secondary private IP address to associate with the Elastic IP address."
  type        = string
  default     = "10.0.0.5"
}