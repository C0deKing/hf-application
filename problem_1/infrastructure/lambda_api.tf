resource "aws_lambda_function" "extract_endpoint" {
  image_uri     = "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}"
  function_name = "${var.environment}-api-extract-endpoint-lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  architectures = ["arm64"]
  image_config {
    command = ["receipt_extractor.api_handler.lambda_handler"]
  }
  depends_on = [
    aws_iam_role_policy_attachment.api_attach_application_role,
    aws_iam_role_policy_attachment.api_attach_kinesis_role,
    null_resource.docker_packaging
  ]
  environment {
    variables = {
      "DYNAMODB_REGION" : var.region
      "DYNAMODB_TABLE_NAME" : aws_dynamodb_table.receipt-data.id,
      "KINESIS_STREAM" : aws_kinesis_stream.process_receipt_stream.name
    }
  }
}