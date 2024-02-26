output "vpc_id" {
  value = "${aws_vpc.vpc.id}"
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.vpc.id]
  }
}

output "subnet_ids" {
  value = data.aws_subnets.subnets.ids
}

output "default_security_group_id" {
  value = aws_security_group.default.id
}