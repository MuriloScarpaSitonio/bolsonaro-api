resource "aws_db_instance" "this" {
  allocated_storage = var.allocated_storage
  engine            = var.engine
  engine_version    = var.engine_version
  instance_class    = var.instance_class
  identifier        = "${var.project_name}-rds-identifier"
  name              = var.name
  username          = var.username
  password          = var.password
  port              = var.port

  parameter_group_name   = aws_db_parameter_group.this.name
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.this.id]

  publicly_accessible         = false
  skip_final_snapshot         = true
  multi_az                    = false
  allow_major_version_upgrade = false

  tags = {
    name = "${var.project_name}-rds"
    env  = terraform.workspace
  }
}


###################################### PARAMETER GROUPS ######################################


# Provides an RDS DB parameter group resource.
# PostgreSQL docs: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.html#Appendix.PostgreSQL.CommonDBATasks.Parameters
resource "aws_db_parameter_group" "this" {
  name   = "${var.project_name}-rds-parameter-group"
  family = var.parameter_group_family

  parameter { #Logs each successful connection.
    name  = "log_connections"
    value = "1"

    # For dynamic use apply_method = "immediate"
    # https://tech.instacart.com/terraforming-rds-part-3-9d81a7e2047f
    apply_method = "immediate"
  }

  parameter { #Automatic log file rotation will occur after N minutes.
    name         = "log_rotation_age"
    value        = 10080 #60*24*7
    apply_method = "immediate"
  }

  parameter { #Sets the client's character set encoding.
    name         = "client_encoding"
    value        = "UTF8"
    apply_method = "immediate"
  }

  tags = {
    name = "${var.project_name}-rds-parameter-group"
    env  = terraform.workspace
  }
}



###################################### SECURITY GROUPS ######################################




resource "aws_security_group" "this" {
  name   = "${var.project_name}-rds-security-group"
  vpc_id = var.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = var.port
    to_port         = var.port
    security_groups = [var.ecs_security_group_id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = var.vpc_cidr_blocks
  }

  tags = {
    name = "${var.project_name}-rds-security-group"
    env  = terraform.workspace
  }
}



###################################### SUBNET GROUPS ######################################



# Provides an RDS DB subnet group resource.
resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-rds-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    name = "${var.project_name}-rds-subnet-group"
    env  = terraform.workspace
  }
}
