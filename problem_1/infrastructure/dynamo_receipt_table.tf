resource "aws_dynamodb_table" "receipt-data" {
  name         = "${var.environment}_receipt-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "request_id"

  attribute {
    name = "request_id"
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