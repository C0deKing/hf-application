resource "aws_lambda_function" "process_receipt" {
  image_uri     = "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}"
  function_name = "${var.environment}-process-receipt-lambda"
  role          = aws_iam_role.process_receipt_role.arn
  package_type  = "Image"
  architectures = ["arm64"]
  memory_size   = 4096
  timeout       = 360
  depends_on    = [
    aws_iam_role_policy_attachment.process_receipt_application_access,
    aws_iam_role_policy_attachment.process_receipt_kinesis,
    null_resource.docker_packaging
  ]
  image_config {
    command = ["receipt_extractor.kinesis_handler.process_receipt"]
  }
  environment {
    variables = {
      "DYNAMODB_REGION" : var.region
      "DYNAMODB_TABLE_NAME" : aws_dynamodb_table.receipt-data.id,
      "KINESIS_STREAM" : aws_kinesis_stream.extract_data_stream.name,
      "S3_BUCKET_NAME" : aws_s3_bucket.receipt_data.id
    }
  }
}

resource "aws_lambda_event_source_mapping" "process_receipt" {
  event_source_arn              = aws_kinesis_stream.process_receipt_stream.arn
  function_name                 = aws_lambda_function.process_receipt.arn
  batch_size                    = 1
  starting_position             = "TRIM_HORIZON"
  maximum_retry_attempts        = 1
  maximum_record_age_in_seconds = 360

  destination_config {
    on_failure {
      destination_arn = aws_sqs_queue.dead_letters.arn
    }
  }
}