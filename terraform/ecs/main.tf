###################################### ELASTIC CONTAINER SERVICE ######################################



resource "aws_ecs_cluster" "this" {
  name = "${var.project_name} ECS"
}

# A task definition is required to run Docker containers in Amazon ECS. 
# You can define multiple containers in a task definition.
# The following are some of the parameters you can specify in a task definition:
#   - The Docker image to use with each container in your task
#   - How much CPU and memory to use with each task or each container within a task
#   - The launch type to use, which determines the infrastructure on which your tasks are hosted
#   - The Docker networking mode to use for the containers in your task
#   - The logging configuration to use for your tasks
#   - Whether the task should continue to run if the container finishes or fails
#   - The command the container should run when it is started
#   - Any data volumes that should be used with the containers in the task
#   - The IAM role that your tasks should use
resource "aws_ecs_task_definition" "this" {
  family = "${var.project_name}-ecs-task-definition" # A unique name for your task definition.

  requires_compatibilities = ["FARGATE"]
  # If using the Fargate launch type, the awsvpc network mode is required.
  network_mode = "awsvpc"

  cpu                = var.fargate_cpu
  memory             = var.fargate_memory
  execution_role_arn = aws_iam_role.task_execution.arn
  container_definitions = jsonencode([
    {
      "name" : "django",
      "image" : var.django_docker_image_url,
      "networkMode" : "awsvpc",
      "essential" : true,
      "cpu" : var.fargate_cpu,
      "memory" : var.fargate_memory,
      "links" : [],
      "portMappings" : [
        {
          "containerPort" : var.django_container_port,
          "hostPort" : 0,
          "protocol" : "tcp"
        }
      ],
      "mountPoints" : [
        {
          "containerPath" : "/app/django/static",
          "sourceVolume" : "django_static_volume"
        }
      ],
      "command" : ["gunicorn", "bolsonaro_api.wsgi:application",
        "--workers=${var.django_gunicorn_number_of_workers}",
      "--bind=:${var.django_container_port}"],
      "environment" : var.django_environment
    },
    {
      "name" : "react",
      "image" : var.react_docker_image_url,
      "networkMode" : "awsvpc",
      "essential" : true,
      "links" : ["django"],
      "portMappings" : [
        {
          "containerPort" : var.react_container_port,
          "hostPort" : 0,
          "protocol" : "tcp"
        }
      ],
      "mountPoints" : [
        {
          "containerPath" : "/app/react/build/static",
          "sourceVolume" : "react_static_volume"
        }
      ]
      "command" : ["serve", "--single", "build", "--listen=${var.react_container_port}"],
      "environment" : var.react_environment
    },
    {
      "name" : "nginx",
      "image" : var.nginx_docker_image_url,
      "essential" : true,
      "cpu" : var.fargate_cpu,
      "memory" : var.fargate_memory / 2,
      "links" : ["django", "react"],
      "portMappings" : [
        {
          "containerPort" : 80,
          "hostPort" : 80,
          "protocol" : "tcp"
        }
      ],
      "mountPoints" : [
        {
          "containerPath" : "/app/django/static",
          "sourceVolume" : "django_static_volume"
        },
        {
          "containerPath" : "/app/react/build/static",
          "sourceVolume" : "react_static_volume"
        }
      ],
    }
  ])
}

resource "aws_ecs_service" "this" {
  name            = "${var.project_name}-ecs-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  iam_role        = aws_iam_role.service.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  depends_on      = [aws_alb_listener.this, aws_iam_role_policy.service]

  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.this.arn
    container_name   = "nginx"
    container_port   = 80
  }

  # Optional: Allow external changes without Terraform plan difference
  # Because we are autoscaling this need to be ignored
  lifecycle {
    ignore_changes = [desired_count]
  }
}
