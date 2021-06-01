###################################### IAM ECS ROLE ######################################



data "aws_iam_policy_document" "ecs_role" {
  version = "2008-10-17"
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com", "ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "host" {
  name               = "${var.project_name}-ECS-Host-IAM-Role"
  assume_role_policy = data.aws_iam_policy_document.ecs_role.json

  tags = {
    name = "${var.project_name}-iam-role-ecs-host"
    env  = terraform.workspace
  }
}

resource "aws_iam_role" "service" {
  name               = "${var.project_name}-ECS-Service-IAM-Role"
  assume_role_policy = data.aws_iam_policy_document.ecs_role.json

  tags = {
    name = "${var.project_name}-iam-role-ecs-service"
    env  = terraform.workspace
  }
}

resource "aws_iam_instance_profile" "this" {
  name = "${var.project_name}-ECS-IAM-Profile"
  path = "/"
  role = aws_iam_role.host.name

  tags = {
    name = "${var.project_name}-iam-instance-profile"
    env  = terraform.workspace
  }
}



###################################### IAM ECS POLICY ######################################



data "aws_iam_policy_document" "ecs_host_policy" {
  statement {
    effect    = "Allow"
    actions   = ["ecs:*", "ec2:*", "elasticloadbalancing:*", "ecr:*", "s3:*", "rds:*"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "host" {
  name   = "${var.project_name}-ECS-Host-IAM-Policy"
  policy = data.aws_iam_policy_document.ecs_host_policy.json
  role   = aws_iam_role.host.id
}


data "aws_iam_policy_document" "ecs_service_policy" {
  statement {
    effect = "Allow"
    actions = ["elasticloadbalancing:Describe*",
      "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
      "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
      "ec2:Describe*",
      "ec2:AuthorizeSecurityGroupIngress",
      "elasticloadbalancing:RegisterTargets",
    "elasticloadbalancing:DeregisterTargets"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "service" {
  name   = "${var.project_name}-ECS-Service-IAM-Policy"
  policy = data.aws_iam_policy_document.ecs_service_policy.json
  role   = aws_iam_role.service.id
}



###################################### IAM ECS TASK EXECUTION ROLE ######################################



data "aws_iam_policy_document" "task_execution_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project_name}-ECS-Task-Execution-IAM-Role"
  assume_role_policy = data.aws_iam_policy_document.task_execution_role.json

  tags = {
    Name = "${var.project_name}-iam-role-ecs-task-execution"
  }
}




###################################### IAM ECS AUTOSCALING ROLE ######################################




data "aws_iam_policy_document" "autoscaling_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["application-autoscaling.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "autoscaling" {
  name               = "${var.project_name}-ECS-Autoscaling-IAM-Role"
  assume_role_policy = data.aws_iam_policy_document.autoscaling_role.json

  tags = {
    Name = "${var.project_name}-iam-role-ecs-autoscaling"
  }
}



###################################### IAM ECS AUTOSCALING POLICY ######################################



data "aws_iam_policy_document" "autoscaling_policy" {
  statement {
    effect    = "Allow"
    actions   = ["ecs:DescribeServices", "ecs:UpdateService"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["cloudwatch:DescribeAlarms"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "autoscaling" {
  name   = "${var.project_name}-ECS-Autoscaling-Policy"
  policy = data.aws_iam_policy_document.autoscaling_policy.json
  role   = aws_iam_role.autoscaling.id
}
