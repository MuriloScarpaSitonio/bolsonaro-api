terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket     = "bolsonaro-api-terraform-state"
    key        = "production/terraform.tfstate"
    region     = "sa-east-1"
    //encrypt = true
  }
}


provider "aws" {
  region = var.aws_region
}


data "aws_availability_zones" "available" {
  state = "available"
}


module "vpc" {
  source = "./vpc"

  project_name = var.project_name

  # VPC with 65,536 possible IP addresses
  # https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
  cidr_block          = var.vpc_cidr_block
  public_cidr_blocks  = var.vpc_public_cidr_blocks
  private_cidr_blocks = var.vpc_private_cidr_blocks

  availability_zones = [
    data.aws_availability_zones.available.names[0],
    data.aws_availability_zones.available.names[1]
  ]
}


module "rds" {
  source = "./rds"

  project_name = var.project_name

  allocated_storage = var.rds_allocated_storage
  engine            = var.rds_engine
  engine_version    = var.rds_engine_version
  instance_class    = var.rds_instance_class
  name              = var.rds_name
  username          = var.rds_username
  port              = var.rds_port

  parameter_group_family = var.rds_parameter_group_family

  vpc_id          = module.vpc.id
  vpc_cidr_blocks = [module.vpc.cidr_block]

  subnet_ids = module.vpc.private_subnet_ids

  ecs_security_group_id = module.ecs.security_group_id
}

module "ecs" {
  source = "./ecs"

  project_name = var.project_name

  django_docker_image_url = var.django_docker_image_url
  django_environment = [
    {
      "name" : "DAJNGO_SECRET_KEY",
      "value" : var.django_secret_key
    },
    {
      "name" : "EMAIL_HOST_USER",
      "value" : var.django_email_host_user
    },
    {
      "name" : "RECAPTCHA_SECRET_KEY",
      "value" : var.django_recaptcha_secret_key
    },
    {
      "name" : "SENDGRID_API_KEY",
      "value" : var.django_sendgrid_api_key
    },
    {
      "name" : "DB_NAME",
      "value" : module.rds.name
    },
    {
      "name" : "DB_USERNAME",
      "value" : module.rds.username
    },
    {
      "name" : "DB_HOST",
      "value" : module.rds.host
    },
    {
      "name" : "DB_PASSWORD",
      "value" : module.rds.password
    }
  ]

  react_docker_image_url = var.react_docker_image_url
  react_environment = [
    {
      "name" : "REACT_APP_RECAPTCHA_SITE_KEY",
      "value" : var.react_recaptcha_site_key
    },
    {
      "name" : "REACT_APP_PIX_KEY",
      "value" : var.react_pix_key
    },
    {
      "name" : "REACT_APP_BASE_API_URL",
      "value" : var.react_base_api_url
    }
  ]

  nginx_docker_image_url = var.nginx_docker_image_url

  vpc_id = module.vpc.id

  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids

  // depends_on = [module.rds.host]
}

module "lambda" {
  source = "./lambda"

  project_name  = var.project_name
  function_name = var.lambda_function_name
  source_dir    = "../aws_lambda"
  handler       = "aws_lambda.post_bolsonaro_api_tweet.lambda_handler"
  env_vars = {
    TWITTER_API_KEY          = var.lambda_twitter_api_key
    TWITTER_API_SECRET_KEY   = var.lambda_twitter_api_secret_key
    TWITTER_API_TOKEN        = var.lambda_twitter_api_token
    TWITTER_API_SECRET_TOKEN = var.lambda_twitter_api_secret_token
  }
}