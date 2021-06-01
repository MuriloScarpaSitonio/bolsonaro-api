# Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual 
# network that you've defined. This virtual network closely resembles a traditional network that 
# you'd operate in your own data center, with the benefits of using the scalable infrastructure of AWS.
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    name = "${var.project_name}-vpc"
    env  = terraform.workspace
  }
}



###################################### SUBNETS ######################################



# A subnet, or subnetwork, is a network inside a network. Subnets make networks more efficient. 
# Through subnetting, network traffic can travel a shorter distance without passing through 
# unnecessary routers to reach its destination.
resource "aws_subnet" "public1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_cidr_blocks[0]
  availability_zone = var.availability_zones[0]

  tags = {
    name = "${var.project_name}-subnet-public1"
    env  = terraform.workspace
  }
}

resource "aws_subnet" "public2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_cidr_blocks[1]
  availability_zone = var.availability_zones[1]

  tags = {
    name = "${var.project_name}-subnet-public2"
    env  = terraform.workspace
  }
}

resource "aws_subnet" "private1" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_cidr_blocks[0]
  availability_zone = var.availability_zones[0]

  tags = {
    name = "${var.project_name}-subnet-private1"
    env  = terraform.workspace
  }
}


resource "aws_subnet" "private2" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_cidr_blocks[1]
  availability_zone = var.availability_zones[1]

  tags = {
    name = "${var.project_name}-subnet-private2"
    env  = terraform.workspace
  }
}



###################################### GATEWAYS ######################################



# An internet gateway is a horizontally scaled, redundant, and highly available VPC component that allows 
# communication between your VPC and the internet.
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    name = "${var.project_name}-vpc-internet-gateway"
    env  = terraform.workspace
  }
}


# An Elastic IP address is a static IPv4 address designed for dynamic cloud computing. 
# An Elastic IP address is allocated to your AWS account, and is yours until you release it. 
# By using an Elastic IP address, you can mask the failure of an instance or software by rapidly 
# remapping the address to another instance in your account.
resource "aws_eip" "this" {
  vpc                       = true
  associate_with_private_ip = var.eip_private_ip_to_associate
  depends_on                = [aws_internet_gateway.this]

  tags = {
    name = "${var.project_name}-vpc-eip"
    env  = terraform.workspace
  }
}


# You can use a NAT device to enable instances in a private subnet to connect to the internet 
# (for example, for software updates) or other AWS services, but prevent the internet from 
# initiating connections with the instances. A NAT device forwards traffic from the instances 
# in the private subnet to the internet or other AWS services, and then sends the 
# response back to the instances.
resource "aws_nat_gateway" "this" {
  subnet_id     = aws_subnet.public1.id
  allocation_id = aws_eip.this.id
  depends_on    = [aws_eip.this]

  tags = {
    name = "${var.project_name}-vpc-nat-gateway"
    env  = terraform.workspace
  }
}


###################################### ROUTES ######################################



# A route table contains a set of rules, called routes, that are used to determine where network 
# traffic from your subnet or gateway is directed.
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  dynamic "route" {
    for_each = var.routes_cidr_blocks

    content {
      cidr_block = route.value
      gateway_id = aws_internet_gateway.this.id
    }
  }

  tags = {
    name = "${var.project_name}-route-table-public"
    env  = terraform.workspace
  }
}


resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  dynamic "route" {
    for_each = var.routes_cidr_blocks

    content {
      cidr_block = route.value
      gateway_id = aws_nat_gateway.this.id
    }
  }

  tags = {
    name = "${var.project_name}-route-table-private"
    env  = terraform.workspace
  }
}


# Provides a resource to create an association between a route table and a subnet or a route 
# table and an internet gateway or virtual private gateway.
resource "aws_route_table_association" "public1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}


resource "aws_route_table_association" "private1" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private.id
}


resource "aws_route_table_association" "private2" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private.id
}


# Provides a resource to create a routing table entry (a route) in a VPC routing table.
resource "aws_route" "nat_gateway" {
  route_table_id         = aws_route_table.private.id
  nat_gateway_id         = aws_nat_gateway.this.id
  destination_cidr_block = var.routes_cidr_blocks[0]
}

resource "aws_route" "internet_gateway" {
  route_table_id         = aws_route_table.public.id
  gateway_id             = aws_internet_gateway.this.id
  destination_cidr_block = var.routes_cidr_blocks[0]
}