resource "aws_lambda_function" "extract_data" {
  image_uri     = "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}"
  function_name = "${var.environment}-extract-data-lambda"
  role          = aws_iam_role.extract_data_role.arn
  package_type  = "Image"
  timeout       = 240
  memory_size   = 10240

  architectures = ["arm64"]
  depends_on    = [
    aws_iam_role_policy_attachment.extract_data_application_access,
    aws_iam_role_policy_attachment.extract_data_kinesis,
    null_resource.docker_packaging
  ]
  image_config {
    command = ["receipt_extractor.kinesis_handler.extract_data"]
  }
  ephemeral_storage {
    size = 2048 # Min 512 MB and the Max 10240 MB
  }
  environment {
    variables = {
      "DYNAMODB_REGION" : var.region
      "DYNAMODB_TABLE_NAME" : aws_dynamodb_table.receipt-data.id,
      "KINESIS_STREAM" : aws_kinesis_stream.extract_data_stream.name,
      "S3_BUCKET_NAME" : aws_s3_bucket.receipt_data.id,
      "HF_HOME" : "/tmp/hf-home/"
    }
  }
}

resource "aws_lambda_event_source_mapping" "extract_data" {
  event_source_arn                   = aws_kinesis_stream.extract_data_stream.arn
  function_name                      = aws_lambda_function.extract_data.arn
  batch_size                         = 4
  maximum_batching_window_in_seconds = 5
  starting_position                  = "LATEST"
  maximum_retry_attempts             = 2
  maximum_record_age_in_seconds      = 3600
  bisect_batch_on_function_error     = true

  destination_config {
    on_failure {
      destination_arn = aws_sqs_queue.dead_letters.arn
    }
  }
}