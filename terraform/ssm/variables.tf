variable "aws_region" {
  description = "The current AWS region"
  type        = string
  default     = "sa-east-1"
}

variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "rds_username" {
  description = "Username for the master DB user"
  type        = string
  sensitive   = true
}

variable "rds_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Secret key for django docker container"
  type        = string
  sensitive   = true
}

variable "django_recaptcha_secret_key" {
  description = "Recaptcha secret key for django docker container"
  type        = string
  sensitive   = true
}

variable "django_sendgrid_api_key" {
  description = "Sendgrid API key for django docker container"
  type        = string
  sensitive   = true
}

variable "lambda_twitter_api_key" {
  description = "Twitter API key for lambda function"
  type        = string
  sensitive   = true
}

variable "lambda_twitter_api_secret_key" {
  description = "Twitter API secret key for lambda function"
  type        = string
  sensitive   = true
}

variable "lambda_twitter_api_token" {
  description = "Twitter API token for lambda function"
  type        = string
  sensitive   = true
}

variable "lambda_twitter_api_secret_token" {
  description = "Twitter API secret token for lambda function"
  type        = string
  sensitive   = true
}

variable "django_admin_username" {
  description = "Django admin username"
  type        = string
  sensitive   = true
}

variable "django_admin_password" {
  description = "Django admin password"
  type        = string
  sensitive   = true
}
