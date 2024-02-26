resource "aws_api_gateway_rest_api" "receipt_api" {
  name        = "${var.environment}-receipt-api"
  description = "API Gateway for the Receipt Extraction API"
}

resource "aws_api_gateway_resource" "receipt_api" {
  rest_api_id = "${aws_api_gateway_rest_api.receipt_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.receipt_api.root_resource_id}"
  path_part   = "receipt"
}

resource "aws_api_gateway_method" "receipt_api_post" {
  rest_api_id   = "${aws_api_gateway_rest_api.receipt_api.id}"
  resource_id   = "${aws_api_gateway_resource.receipt_api.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "receipt_api_post" {
  rest_api_id = "${aws_api_gateway_rest_api.receipt_api.id}"
  resource_id = "${aws_api_gateway_method.receipt_api_post.resource_id}"
  http_method = "${aws_api_gateway_method.receipt_api_post.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.extract_endpoint.invoke_arn}"
}

resource "aws_api_gateway_method" "receipt_api_get" {
  rest_api_id   = "${aws_api_gateway_rest_api.receipt_api.id}"
  resource_id   = "${aws_api_gateway_resource.receipt_api.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "receipt_api_get" {
  rest_api_id = "${aws_api_gateway_rest_api.receipt_api.id}"
  resource_id = "${aws_api_gateway_method.receipt_api_get.resource_id}"
  http_method = "${aws_api_gateway_method.receipt_api_get.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.extract_endpoint.invoke_arn}"
}


resource "aws_api_gateway_deployment" "receipt_api" {
  depends_on = [
    aws_api_gateway_integration.receipt_api_post
  ]

  triggers = {
    redeployment = data.external.project_version.result.version
  }

  lifecycle {
    create_before_destroy = true
  }

  rest_api_id = "${aws_api_gateway_rest_api.receipt_api.id}"
  stage_name  = "PROD"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.extract_endpoint.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.receipt_api.execution_arn}/*/*"
}