output "arn" {
  value = aws_db_instance.this.arn
}

output "id" {
  value = aws_db_instance.this.id
}

output "host" {
  value = aws_db_instance.this.address
}

output "name" {
  value = aws_db_instance.this.name
}

output "port" {
  value = aws_db_instance.this.port
}

output "username" {
  value = aws_db_instance.this.username
}

output "password" {
  value = aws_db_instance.this.password
}

output "security_group_id" {
  value = aws_security_group.this.id
}