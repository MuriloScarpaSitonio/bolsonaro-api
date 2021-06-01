variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "aws_region" {
  description = "The current AWS region"
  type        = string
  default     = "sa-east-1"
}

variable "vpc_cidr_block" {
  description = "VPC instance Classless Inter-Domain Routing block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_public_cidr_blocks" {
  description = "Two public Classless Inter-Domain Routing block"
  type        = list(string)
  default     = ["10.0.0.0/24", "10.0.1.0/24"] # ["192.168.0.0/24", "192.168.1.0/24"]

  validation {
    # length(var.vpc_public_cidr_blocks) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.vpc_public_cidr_blocks) > 1 && length(var.vpc_public_cidr_blocks) < 3
    error_message = "Must be a list of two values because we have two public subnets."
  }
}

variable "vpc_private_cidr_blocks" {
  description = "Two private instance Classless Inter-Domain Routing block"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"] #["192.168.2.0/24", "192.168.3.0/24"]

  validation {
    # length(var.vpc_private_cidr_blocks) == 2 -> Error (?): An argument definition must end with a newline.
    condition     = length(var.vpc_private_cidr_blocks) > 1 && length(var.vpc_private_cidr_blocks) < 3
    error_message = "Must be a list of two values because we have two private subnets."
  }
}

variable "rds_allocated_storage" {
  description = "The RDS allocated storage in gibibytes"
  type        = number
  default     = 5
}

variable "rds_engine" {
  description = "The RDS engine to use"
  type        = string
  default     = "postgres"
}

variable "rds_engine_version" {
  description = "The RDS engine version to use"
  type        = string
  default     = "13.2"
}

variable "rds_instance_class" {
  description = "The instance type of the RDS"
  type        = string
  default     = "db.t2.micro"
}

variable "rds_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
}

variable "rds_username" {
  description = "Username for the master DB user"
  type        = string
}

variable "rds_port" {
  description = "The database port"
  type        = number
  default     = 5432
}

variable "rds_parameter_group_family" {
  description = "The family of the DB parameter group"
  type        = string
  default     = "postgres13"
}

variable "django_docker_image_url" {
  description = "Image URL for the django docker image"
  type        = string
}

variable "django_secret_key" {
  description = "Secret key for django docker container"
  type        = string
}

variable "django_email_host_user" {
  description = "E-mail host for django docker container"
  type        = string
}

variable "django_recaptcha_secret_key" {
  description = "Recaptcha secret key for django docker container"
  type        = string
}

variable "django_sendgrid_api_key" {
  description = "Sendgrid API key for django docker container"
  type        = string
}

variable "lambda_twitter_api_key" {
  description = "Twitter API key for lambda function"
  type        = string
}

variable "lambda_twitter_api_secret_key" {
  description = "Twitter API secret key for lambda function"
  type        = string
}

variable "lambda_twitter_api_token" {
  description = "Twitter API token for lambda function"
  type        = string
}

variable "lambda_twitter_api_secret_token" {
  description = "Twitter API secret token for lambda function"
  type        = string
}

variable "react_docker_image_url" {
  description = "Image URL for the react docker image"
  type        = string
}

variable "react_recaptcha_site_key" {
  description = "Recaptcha site key for react docker container"
  type        = string
}

variable "react_pix_key" {
  description = "Recaptcha PIX key for react docker container"
  type        = string
}

variable "react_base_api_url" {
  description = "Base django API URL for react docker container"
  type        = string
  default     = "/api/v1"
}

variable "nginx_docker_image_url" {
  description = "Image URL for the nginx docker image"
  type        = string
}

variable "lambda_function_name" {
  description = "The naome of the lambda function"
  type        = string
  default     = "post_bolsonaro_api_tweet"
}