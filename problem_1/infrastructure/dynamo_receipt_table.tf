resource "aws_dynamodb_table" "receipt-data" {
  name         = "${var.environment}_receipt-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "sort_key"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "sort_key"
    type = "S"
  }



  ttl {
    attribute_name = "expire_at"
    enabled        = true
  }

  tags = {
    Name        = "${var.environment}_receipt-data"
    Environment = var.environment
  }
}