locals {
  parameter_base_name = "/${var.project_name}/${terraform.workspace}"
}

data "aws_ssm_parameter" "rds_username" {
  name = "${local.parameter_base_name}/rds-username"
}

data "aws_ssm_parameter" "rds_name" {
  name = "${local.parameter_base_name}/rds-name"
}

data "aws_ssm_parameter" "django_secret_key" {
  name = "${local.parameter_base_name}/django-secret-key"
}

data "aws_ssm_parameter" "django_recaptcha_secret_key" {
  name = "${local.parameter_base_name}/django-recaptcha-secret-key"
}

data "aws_ssm_parameter" "django_sendgrid_api_key" {
  name = "${local.parameter_base_name}/django-sendgrid-api-key"
}

data "aws_ssm_parameter" "lambda_twitter_api_key" {
  name = "${local.parameter_base_name}/lambda-twitter-api-key"
}

data "aws_ssm_parameter" "lambda_twitter_api_secret_key" {
  name = "${local.parameter_base_name}/lambda-twitter-api-secret-key"
}

data "aws_ssm_parameter" "lambda_twitter_api_token" {
  name = "${local.parameter_base_name}/lambda-twitter-api-token"
}

data "aws_ssm_parameter" "lambda_twitter_api_secret_token" {
  name = "${local.parameter_base_name}/lambda-twitter-api-secret-token"
}

data "aws_ssm_parameter" "django_admin_username" {
  name = "${local.parameter_base_name}/django-admin-username"
}

data "aws_ssm_parameter" "django_admin_password" {
  name = "${local.parameter_base_name}/django-admin-password"
}
