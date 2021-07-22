terraform {
  required_version = ">= 0.15"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.45"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  parameter_base_name = "/${var.project_name}/${terraform.workspace}"
}


# Parameter Store, a capability of AWS Systems Manager, provides secure, 
# hierarchical storage for configuration data management and secrets management. 
# You can store data such as passwords, database strings, Amazon Machine Image (AMI) IDs, 
# and license codes as parameter values. You can store values as plain text or encrypted data. 
# You can reference Systems Manager parameters in your scripts, commands, SSM documents, and 
# configuration and automation workflows by using the unique name that you specified when you 
# created the parameter.
resource "aws_ssm_parameter" "rds_username" {
  name  = "${local.parameter_base_name}/rds-username"
  type  = "String"
  value = var.rds_username

  tags = {
    name = "${var.project_name}-ssm-parameter-rds-username"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "rds_name" {
  name  = "${local.parameter_base_name}/rds-name"
  type  = "String"
  value = var.rds_name

  tags = {
    name = "${var.project_name}-ssm-parameter-rds-name"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "django_secret_key" {
  name  = "${local.parameter_base_name}/django-secret-key"
  type  = "String"
  value = var.django_secret_key

  tags = {
    name = "${var.project_name}-ssm-parameter-django-secret-key"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "django_recaptcha_secret_key" {
  name  = "${local.parameter_base_name}/django-recaptcha-secret-key"
  type  = "String"
  value = var.django_recaptcha_secret_key

  tags = {
    name = "${var.project_name}-ssm-parameter-django-recaptcha-secret-key"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "django_sendgrid_api_key" {
  name  = "${local.parameter_base_name}/django-sendgrid-api-key"
  type  = "String"
  value = var.django_sendgrid_api_key

  tags = {
    name = "${var.project_name}-ssm-parameter-django-sendgrid-api-key"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "lambda_twitter_api_key" {
  name  = "${local.parameter_base_name}/lambda-twitter-api-key"
  type  = "String"
  value = var.lambda_twitter_api_key

  tags = {
    name = "${var.project_name}-ssm-parameter-lambda-twitter-api-key"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "lambda_twitter_api_secret_key" {
  name  = "${local.parameter_base_name}/lambda-twitter-api-secret-key"
  type  = "String"
  value = var.lambda_twitter_api_secret_key

  tags = {
    name = "${var.project_name}-ssm-parameter-lambda-twitter-api-secret-key"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "lambda_twitter_api_token" {
  name  = "${local.parameter_base_name}/lambda-twitter-api-token"
  type  = "String"
  value = var.lambda_twitter_api_token

  tags = {
    name = "${var.project_name}-ssm-parameter-lambda-twitter-api-token"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "lambda_twitter_api_secret_token" {
  name  = "${local.parameter_base_name}/lambda-twitter-api-secret-token"
  type  = "String"
  value = var.lambda_twitter_api_secret_token

  tags = {
    name = "${var.project_name}-ssm-parameter-lambda-twitter-api-secret-token"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "django_admin_username" {
  name  = "${local.parameter_base_name}/django-admin-username"
  type  = "String"
  value = var.django_admin_username

  tags = {
    name = "${var.project_name}-ssm-parameter-django-admin-username"
    env  = terraform.workspace
  }
}

resource "aws_ssm_parameter" "django_admin_password" {
  name  = "${local.parameter_base_name}/django-admin-password"
  type  = "String"
  value = var.django_admin_password

  tags = {
    name = "${var.project_name}-ssm-parameter-django-admin-password"
    env  = terraform.workspace
  }
}
