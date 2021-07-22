variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "aws_region" {
  description = "The current AWS region"
  type        = string
}

variable "django_docker_image_url" {
  description = "Image URL for the django docker image"
  type        = string
}

variable "django_gunicorn_number_of_workers" {
  # https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
  description = "The suggested number of workers is (2*CPU)+1."
  type        = number
  default     = 3
}

variable "django_container_port" {
  description = "The port that the django container will expose."
  type        = number
  default     = 8000
}

variable "django_environment" {
  description = "The environment variables to pass to the django container."
  type = list(object({
    name  = string
    value = string
  }))
}

#variable "react_environment" {
#  description = "The environment variables to pass to the react container."
#  type = list(object({
#    name  = string
#    value = string
#  }))
#}

#variable "react_container_port" {
#  description = "The port that the react container will expose."
#  type        = number
#  default     = 3000
#}

#variable "react_docker_image_url" {
#  description = "Image URL for the react docker image"
#  type        = string
#}

variable "nginx_docker_image_url" {
  description = "Image URL for the nginx docker image"
  type        = string
}

variable "nginx_container_port" {
  description = "The port that the react container will expose."
  type        = number
  default     = 80
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  type        = number
  default     = 1024
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  type        = number
  default     = 2048
}

variable "desired_count" {
  description = "Number of docker containers to run"
  type        = number
  default     = 4
}


// variable "security_groups_ids" {
//  description = "Other security groups IDs for the ECS service."
//  type        = list(string)
//}

variable "private_subnet_ids" {
  description = "A list of privated subnet IDs"
  type        = list(string)

  validation {
    # length(var.private_subnet_ids) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.private_subnet_ids) > 1 && length(var.private_subnet_ids) < 3
    error_message = "Must be a list of two values because we have two private subnets."
  }
}

variable "public_subnet_ids" {
  description = "A list of privated subnet IDs"
  type        = list(string)

  validation {
    # length(var.public_subnet_ids) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.public_subnet_ids) > 1 && length(var.public_subnet_ids) < 3
    error_message = "Must be a list of two values because we have two public subnets."
  }
}

variable "vpc_id" {
  description = "VPC id for the security group"
  type        = string
}

variable "nginx_alb_health_check_path" {
  description = "ALB health check path at nginx"
  type        = string
  default     = "/health"
}

variable "min_capacity" {
  description = "Minimum number of task to run"
  type        = number
  default     = 2
}

variable "max_capacity" {
  description = "Maximum number of task to run"
  type        = number
  default     = 8
}

variable "ecs_security_group_id" {
  description = "Security group ID to ECS service. This is not created inside the module because it's shared with RDS"
  type        = string
}

variable "alb_security_group_id" {
  description = "Security group ID to ALB. This is not created inside the module because it's shared with ECS security group"
  type        = string
}
