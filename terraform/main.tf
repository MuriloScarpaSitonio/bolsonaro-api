terraform {
  required_version = ">= 0.15"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.45"
    }
  }

  backend "s3" {
    bucket  = "bolsonaro-api-tf-state"
    key     = "default/terraform.tfstate"
    region  = "sa-east-1"
    encrypt = true
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

resource "random_password" "this" {
  length      = 32
  special     = true
  min_special = 6
  lower       = true
  number      = true
  upper       = true
}

module "rds" {
  source = "./rds"

  project_name = var.project_name

  allocated_storage = var.rds_allocated_storage
  engine            = var.rds_engine
  engine_version    = var.rds_engine_version
  instance_class    = var.rds_instance_class
  name              = data.aws_ssm_parameter.rds_name.value
  username          = data.aws_ssm_parameter.rds_username.value
  port              = var.rds_port
  password          = random_password.this.result

  parameter_group_family = var.rds_parameter_group_family

  vpc_id          = module.vpc.id
  vpc_cidr_blocks = [module.vpc.cidr_block]

  subnet_ids = module.vpc.private_subnet_ids

  ecs_security_group_id = aws_security_group.ecs.id
}

module "s3_cloudfront" {
  source = "./s3-cloudfront"

  project_name = var.project_name
}

module "ecs" {
  source = "./ecs"

  project_name = var.project_name

  django_docker_image_url = var.django_docker_image_url
  django_environment = [
    {
      "name" : "DAJNGO_SECRET_KEY",
      "value" : data.aws_ssm_parameter.django_secret_key.value
    },
    {
      "name" : "EMAIL_HOST_USER",
      "value" : var.django_email_host_user
    },
    {
      "name" : "RECAPTCHA_SECRET_KEY",
      "value" : data.aws_ssm_parameter.django_recaptcha_secret_key.value
    },
    {
      "name" : "SENDGRID_API_KEY",
      "value" : data.aws_ssm_parameter.django_sendgrid_api_key.value
    },
    {
      "name" : "DATABASE_ENGINE",
      "value" : var.django_db_engine
    },
    {
      "name" : "DATABASE_PORT",
      "value" : var.rds_port
    },
    {
      "name" : "DATABASE_NAME",
      "value" : data.aws_ssm_parameter.rds_name.value
    },
    {
      "name" : "DATABASE_USER",
      "value" : data.aws_ssm_parameter.rds_username.value
    },
    {
      "name" : "DATABASE_HOST",
      "value" : module.rds.host
    },
    {
      "name" : "DATABASE_PASSWORD",
      "value" : random_password.this.result
    },
    {
      "name" : "AWS_ACCESS_KEY_ID",
      "value" : var.AWS_ACCESS_KEY_ID
    },
    {
      "name" : "AWS_SECRET_ACCESS_KEY",
      "value" : var.AWS_SECRET_ACCESS_KEY
    },
    {
      "name" : "AWS_REGION_NAME",
      "value" : var.aws_region
    },
    {
      "name" : "AWS_STORAGE_BUCKET_NAME",
      "value" : module.s3_cloudfront.django_static_files_bucket_name
    },
    {
      "name" : "ADMIN_USERNAME",
      "value" : data.aws_ssm_parameter.django_admin_username.value
    },
    {
      "name" : "ADMIN_PASSWORD",
      "value" : data.aws_ssm_parameter.django_admin_password.value
    },
  ]

  #react_docker_image_url = var.react_docker_image_url
  #react_environment = [
  #  {
  #    "name" : "REACT_APP_RECAPTCHA_SITE_KEY",
  #    "value" : var.react_recaptcha_site_key
  #  },
  #  {
  #    "name" : "REACT_APP_PIX_KEY",
  #    "value" : var.react_pix_key
  #  },
  #  {
  #    "name" : "REACT_APP_BASE_API_URL",
  #    "value" : var.react_base_api_url
  #  }
  #]

  nginx_docker_image_url = var.nginx_docker_image_url

  aws_region = var.aws_region

  vpc_id = module.vpc.id

  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids

  ecs_security_group_id = aws_security_group.ecs.id
  alb_security_group_id = aws_security_group.alb.id

  depends_on = [module.rds, module.s3_cloudfront]
}

#module "lambda" {
#  source = "./lambda"

#  project_name  = var.project_name
#  function_name = var.lambda_function_name
#  source_dir    = "../aws_lambda"
#  handler       = "aws_lambda.post_bolsonaro_api_tweet.lambda_handler"
#  env_vars = {
#    BOLSONARO_API_BASE_URL   = "${module.ecs.alb_dns_name}/api/v1"
#    TWITTER_API_KEY          = data.aws_ssm_parameter.lambda_twitter_api_key.value
#    TWITTER_API_SECRET_KEY   = data.aws_ssm_parameter.lambda_twitter_api_secret_key.value
#    TWITTER_API_TOKEN        = data.aws_ssm_parameter.lambda_twitter_api_token.value
#    TWITTER_API_SECRET_TOKEN = data.aws_ssm_parameter.lambda_twitter_api_secret_token.value
#  }

#  depends_on = [module.ecs]
#}
