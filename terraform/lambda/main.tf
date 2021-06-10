locals {
  function_name = "${var.project_name}-${var.function_name}-${terraform.workspace}"
  zip_path      = "${path.cwd}/.deploy/lambdas"
  zip_file      = "${local.zip_path}/${local.function_name}.zip"
  s3_key        = "lambda/${terraform.workspace}/${var.project_name}/${var.function_name}.zip"
}



###################################### LAMBDA FUNCTION ######################################



# AWS Lambda is a serverless compute service that lets you run code without provisioning 
# or managing servers, creating workload-aware cluster scaling logic, maintaining event 
# integrations, or managing runtimes. With Lambda, you can run code for virtually any 
# type of application or backend service - all with zero administration. 
# Just upload your code as a ZIP file or container image, and Lambda automatically and 
# precisely allocates compute execution power and runs your code based on the incoming 
# request or event, for any scale of traffic.
resource "aws_lambda_function" "this" {

  function_name    = local.function_name
  role             = aws_iam_role.this.arn
  runtime          = var.runtime
  s3_bucket        = aws_s3_bucket.this.id
  s3_key           = local.s3_key
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  memory_size      = var.memory_size
  timeout          = var.timeout
  handler          = var.handler

  environment {
    variables = merge(var.env_vars,
      {
        LOG_LEVEL = "INFO"
      }
    )
  }

  depends_on = [aws_iam_policy.this, aws_cloudwatch_log_group.this, aws_s3_bucket_object.lambda_zip]

  tags = {
    name = "${var.project_name}-lambda-function"
    env  = terraform.workspace
  }
}

# Gives an external source (like a CloudWatch Event Rule, SNS, or S3) permission to access 
# the Lambda function.
resource "aws_lambda_permission" "allow_cloudwatch" {

  for_each = { for i, v in [
    aws_cloudwatch_event_rule.run_at_8am,
    aws_cloudwatch_event_rule.run_at_18pm
  ] : i => v }

  statement_id  = "AllowExecutionFromCloudWatchAt8am"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
  source_arn    = each.value.arn
}


###################################### CLOUDWATCH ######################################



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

# An event indicates a change in an environment such as an AWS environment, 
# a SaaS partner service or application, or one of your applications or services.
# You can also set up scheduled events that are generated on a periodic basis.
resource "aws_cloudwatch_event_rule" "run_at_8am" {
  name                = "${local.function_name}-everyday-at-8am"
  description         = "Fires everyday at 8am"
  schedule_expression = "cron(0 8 * * *)"

  tags = {
    name = "${local.function_name}-cloudwatch-rule-to-run-at-8am"
    env  = terraform.workspace
  }
}

resource "aws_cloudwatch_event_rule" "run_at_18pm" {
  name                = "${local.function_name}-everyday-at-18pm"
  description         = "Fires everyday at 18pm"
  schedule_expression = "cron(0 18 * * *)"

  tags = {
    name = "${local.function_name}-cloudwatch-rule-to-run-at-18pm"
    env  = terraform.workspace
  }
}

# A target is a resource or endpoint that EventBridge sends an event to when the event matches 
# the event pattern defined for a rule. The rule processes the event data and sends the pertinent 
# information to the target. To deliver event data to a target, EventBridge needs permission to 
# access the target resource. You can define up to five targets for each rule.
resource "aws_cloudwatch_event_target" "run_lambda_function" {
  for_each = { for i, v in [
    { "rule" : aws_cloudwatch_event_rule.run_at_8am, "input" : "{\"entity_name\":\"quotes\"}" },
    { "rule" : aws_cloudwatch_event_rule.run_at_18pm, "input" : "{\"entity_name\":\"actions\"}" }
  ] : i => v }

  rule  = each.value.rule.id
  arn   = aws_lambda_function.this.arn
  input = each.value.input
}




###################################### S3 ######################################


# The null_resource resource implements the standard resource lifecycle but 
# takes no further action. The triggers argument allows specifying an arbitrary 
# set of values that, when changed, will cause the resource to be replaced.
resource "null_resource" "install_requirements" {
  triggers = {
    requirements_base       = filebase64sha256("${var.source_dir}/requirements/base.txt")
    requirements_production = filebase64sha256("${var.source_dir}/requirements/production.txt")
    function                = filebase64sha256("${var.source_dir}/post_bolsonaro_api_tweet.py")
  }

  provisioner "local-exec" {
    command = "terraform/${path.module}/install_requirements.sh ${var.source_dir}"
  }
}

# Generates an archive from content, a file, or directory of files.
data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = local.zip_file

  depends_on = [null_resource.install_requirements]
}

resource "aws_s3_bucket" "this" {
  bucket = "${var.project_name}-${terraform.workspace}-lambda-bucket"

  tags = {
    name = "${var.project_name}-lambda-s3-bucket"
    env  = terraform.workspace
  }
}

resource "aws_s3_bucket_object" "lambda_zip" {
  bucket = aws_s3_bucket.this.id
  key    = local.s3_key
  source = local.zip_file
  etag   = data.archive_file.lambda_package.output_base64sha256

  depends_on = [data.archive_file.lambda_package]

  tags = {
    name = "${var.project_name}-s3-object-lambda-zip"
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
