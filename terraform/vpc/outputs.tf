output "id" {
  value = aws_vpc.this.id
}

output "arn" {
  value = aws_vpc.this.arn
}

output "cidr_block" {
  value = aws_vpc.this.cidr_block
}

output "public_subnet_ids" {
  value = [aws_subnet.public1.id, aws_subnet.public2.id]
}

output "private_subnet_ids" {
  value = [aws_subnet.private1.id, aws_subnet.private2.id]
}

output "internet_gateway_id" {
  value = aws_internet_gateway.this.id
}

