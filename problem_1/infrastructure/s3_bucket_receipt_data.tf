resource "aws_s3_bucket" "receipt_data" {
  bucket = "${var.environment}-receipt-data-${var.region}"

  tags = {
    Name        = "${var.environment}_receipt-data"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.receipt_data.id

  rule {
    id = "expire-app-data"

    filter {
      prefix = "images/"
    }

    expiration {
      days = var.expiration_days
    }

    status = "Enabled"
  }
}