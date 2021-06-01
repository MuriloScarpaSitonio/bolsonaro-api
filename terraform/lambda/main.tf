locals {
  function_name = "${var.project_name}-${var.function_name}-${terraform.workspace}"
  zip_path      = "${path.cwd}/.deploy/lambdas"
  zip_file      = "${local.zip_path}/${local.function_name}.zip"
  s3_key        = "lambda/${terraform.workspace}/${var.project_name}/${var.function_name}.zip"
}



###################################### LAMBDA FUNCTION ######################################



resource "aws_lambda_function" "this" {

  function_name    = local.function_name
  role             = aws_iam_role.this.arn
  runtime          = var.runtime
  s3_bucket        = aws_s3_bucket.this.id
  s3_key           = local.s3_key
  source_code_hash = data.external.code.result.md5sum
  memory_size      = var.memory_size
  timeout          = var.timeout

  environment {
    variables = merge(var.env_vars,
      {
        log_level = "INFO"
      }
    )
  }

  depends_on = [aws_iam_policy.this, aws_cloudwatch_log_group.this, aws_s3_bucket_object.code]

  tags = {
    name = "${var.project_name}-lambda-function"
    env  = terraform.workspace
  }
}


###################################### CLOUDWATCH LOGS ######################################



# You can use Amazon CloudWatch Logs to monitor, store, and access your log files from AWS.
# CloudWatch Logs enables you to centralize the logs from all of your systems, applications, 
# and AWS services that you use, in a single, highly scalable service.
resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = var.log_retention

  tags = {
    name = "${local.function_name}-cloudwatch-log-group"
    env  = terraform.workspace
  }
}




###################################### S3 ######################################



data "external" "code" {
  program = concat(["python3", "terraform/${path.module}/lambda_packer.py",
  local.zip_file, "--requirements=${var.requirements}"], var.source_files)
  working_dir = "../"
}

resource "aws_s3_bucket" "this" {
  bucket = "${var.project_name}-${terraform.workspace}-lambda-bucket"

  tags = {
    name = "${var.project_name}-lambda-s3-bucket"
    env  = terraform.workspace
  }
}

resource "aws_s3_bucket_object" "code" {
  bucket = aws_s3_bucket.this.id
  key    = local.s3_key
  source = local.zip_file
  etag   = data.external.code.result.md5sum

  depends_on = [data.external.code]

  tags = {
    name = "${var.project_name}-lambda-s3-code"
    env  = terraform.workspace
  }
}



###################################### IAM ######################################



data "aws_iam_policy_document" "lambda_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name               = "${local.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_role.json

  tags = {
    Name = "${local.function_name}-iam-role"
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "this" {
  name        = "${local.function_name}-policy"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_policy.json
}
