
resource "aws_iam_role" "lambda_role" {
  name               = "${var.environment}-api-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_role_policy_attachment" "api_attach_application_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.application_iam_policy.arn
}

resource "aws_iam_role_policy_attachment" "api_attach_kinesis_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.api_kinesis_policy.arn
}