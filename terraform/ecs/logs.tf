resource "aws_cloudwatch_log_group" "django" {
  name              = "/ecs/${var.project_name}/django"
  retention_in_days = 30

  tags = {
    name = "${var.project_name}-django-ecs-logs"
    env  = terraform.workspace
  }
}

resource "aws_cloudwatch_log_stream" "django" {
  name           = "${var.project_name}-django-log-stream"
  log_group_name = aws_cloudwatch_log_group.django.name
}

resource "aws_cloudwatch_log_group" "nginx" {
  name              = "/ecs/${var.project_name}/nginx"
  retention_in_days = 30

  tags = {
    name = "${var.project_name}-nginx-ecs-logs"
    env  = terraform.workspace
  }
}

resource "aws_cloudwatch_log_stream" "nginx" {
  name           = "${var.project_name}-nginx-log-stream"
  log_group_name = aws_cloudwatch_log_group.nginx.name
}
