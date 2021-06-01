output "alb_dns_name" {
  value = aws_alb.this.dns_name
}

output "security_group_id" {
  value = aws_security_group.ecs.id
}