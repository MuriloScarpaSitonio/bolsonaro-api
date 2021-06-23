variable "aws_region" {
  description = "The current AWS region"
  type        = string
  default     = "sa-east-1"
}

variable "bucket_name" {
  description = "The name of the s3 bucket which will contain our infra state"
  type        = string
}

variable "key_name" {
  description = "Path to the state file inside the S3 bucket"
  type        = string
}