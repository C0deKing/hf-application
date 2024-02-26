//AWS
region      = "us-east-2"
environment = "hf-application-staging"

/* module networking */
vpc_cidr             = "10.0.0.0/16"
public_subnets_cidr  = ["10.0.1.0/24"] //, "10.0.2.0/24", "10.0.3.0/24"] //List of Public subnet cidr range
private_subnets_cidr = ["10.0.11.0/24"] //, "10.0.12.0/24", "10.0.13.0/24"] //List of private subnet cidr range
availability_zones   = ["us-east-2a"] // "us-east-2b", "us-east-2c"] //List of the AZs to launch subnets in