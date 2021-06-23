output "arn" {
  value = aws_db_instance.this.arn
}

output "id" {
  value = aws_db_instance.this.id
}

output "host" {
  value = aws_db_instance.this.address
}