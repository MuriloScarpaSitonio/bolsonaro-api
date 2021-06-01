# A load balancer serves as the single point of contact for clients. 
# The load balancer distributes incoming application traffic across multiple targets,
# such as EC2 instances, in multiple Availability Zones. 
# This increases the availability of your application. 
# You add one or more listeners to your load balancer.
resource "aws_alb" "this" {
  name               = "${var.project_name}-ALB"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  tags = {
    name = "${var.project_name}-alb"
    env  = terraform.workspace
  }
}

# Each target group is used to route requests to one or more registered targets. 
# When you create each listener rule, you specify a target group and conditions. 
# When a rule condition is met, traffic is forwarded to the corresponding target group. 
# You can create different target groups for different types of requests.
resource "aws_alb_target_group" "this" {
  name     = "${var.project_name}-ALB-Target-Group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  # health_check {
  #  path                = var.health_check_path
  #  matcher             = "200"
  # }

  tags = {
    name = "${var.project_name}-alb-target-group"
    env  = terraform.workspace
  }
}

# A listener is a process that checks for connection requests, using the protocol and 
# port that you configure. The rules that you define for a listener determine how the 
# load balancer routes requests to its registered targets.
resource "aws_alb_listener" "this" {
  load_balancer_arn = aws_alb.this.id
  port              = 80
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.this]

  # Redirect all traffic from the ALB to the target group
  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.this.arn
  }

  tags = {
    name = "${var.project_name}-alb-listener"
    env  = terraform.workspace
  }
}