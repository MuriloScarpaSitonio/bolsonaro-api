locals {
  django_static_files_bucket_name = "${var.project_name}-django-static"
}


resource "aws_s3_bucket" "this" {
  bucket = local.django_static_files_bucket_name

  tags = {
    name = "${local.django_static_files_bucket_name}-s3-bucket"
    env  = terraform.workspace
  }
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Sid"     = "PublicRead"
        Principal = "*"
        Effect    = "Allow"
        Action    = ["s3:GetObject"]
        Resource  = ["${aws_s3_bucket.this.arn}/*"]
      }
    ]
  })
}
