resource "aws_kinesis_stream" "process_receipt_stream" {
  name = "${var.environment}_process-receipt"

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_kinesis_stream" "extract_data_stream" {
  name = "${var.environment}_extract-data"

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  tags = {
    Environment = var.environment
  }
}