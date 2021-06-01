variable "aws_region" {
  description = "The current AWS region"
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the s3 bucket which will contain our infra state"
  type        = string
}