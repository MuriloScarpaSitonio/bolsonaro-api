# With target tracking scaling policies, you select a scaling metric and set a target value. 
# Amazon EC2 Auto Scaling creates and manages the CloudWatch alarms that trigger the scaling 
# policy and calculates the scaling adjustment based on the metric and the target value. 
resource "aws_appautoscaling_target" "this" {
  service_namespace  = "ecs"
  resource_id        = "service/${aws_ecs_cluster.this.name}/${aws_ecs_service.this.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.autoscaling.arn
  min_capacity       = var.min_capacity
  max_capacity       = var.max_capacity
}

# The scaling policy adds or removes capacity as required to keep the metric at, or close to, 
# the specified target value. In addition to keeping the metric close to the target value, 
# a target tracking scaling policy also adjusts to changes in the metric due to a changing load pattern.
resource "aws_appautoscaling_policy" "up" {
  name               = "${var.project_name} Autoscaling Policy up"
  service_namespace  = aws_appautoscaling_target.this.service_namespace
  resource_id        = aws_appautoscaling_target.this.resource_id
  scalable_dimension = aws_appautoscaling_target.this.scalable_dimension

  depends_on = [aws_appautoscaling_target.this]

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Maximum"

    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = 1
    }
  }
}


resource "aws_appautoscaling_policy" "down" {
  name               = "${var.project_name} Autoscaling Policy down"
  service_namespace  = aws_appautoscaling_target.this.service_namespace
  resource_id        = aws_appautoscaling_target.this.resource_id
  scalable_dimension = aws_appautoscaling_target.this.scalable_dimension

  depends_on = [aws_appautoscaling_target.this]

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Maximum"

    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = -1
    }
  }
}

# Metrics are data about the performance of your systems.
# Amazon CloudWatch can load all the metrics in your account for search, graphing, and alarms.
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project_name} high CPU CloudWatch Metric alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = "85"

  dimensions = {
    ClusterName = aws_ecs_cluster.this.name
    ServiceName = aws_ecs_service.this.name
  }

  alarm_actions = [aws_appautoscaling_policy.up.arn]

  tags = {
    Name = "${var.project_name}-cloudwatch-metric-alrm-cpu-high"
  }
}


resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "${var.project_name} low CPU CloudWatch Metric alarm"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = "10"

  dimensions = {
    ClusterName = aws_ecs_cluster.this.name
    ServiceName = aws_ecs_service.this.name
  }

  alarm_actions = [aws_appautoscaling_policy.down.arn]

  tags = {
    name = "${var.project_name}-cloudwatch-metric-alrm-cpu-down"
    env  = terraform.workspace
  }
}

