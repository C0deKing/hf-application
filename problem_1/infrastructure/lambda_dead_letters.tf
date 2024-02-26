resource "aws_lambda_function" "dead_letters" {
  image_uri     = "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}"
  function_name = "${var.environment}-dead-letter-lambda"
  role          = aws_iam_role.dead_letter_role.arn
  package_type  = "Image"
  architectures = ["arm64"]
  depends_on    = [
    null_resource.docker_packaging
  ]
  image_config {
    command = ["receipt_extractor.sns_handler.process_error"]
  }
  environment {
    variables = {
      "DYNAMODB_REGION" : var.region
      "DYNAMODB_TABLE_NAME" : aws_dynamodb_table.receipt-data.id,
      "S3_BUCKET_NAME" : aws_s3_bucket.receipt_data.id
    }
  }
}

resource "aws_lambda_event_source_mapping" "dead_letters" {
  event_source_arn                   = aws_sqs_queue.dead_letters.arn
  function_name                      = aws_lambda_function.dead_letters.arn
  batch_size                         = 10
  maximum_batching_window_in_seconds = 5
}