resource "aws_iam_role" "extract_data_role" {
  name               = "${var.environment}-extract-data-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_role_policy_attachment" "extract_data_application_access" {
  role       = aws_iam_role.extract_data_role.name
  policy_arn = aws_iam_policy.application_iam_policy.arn
}

resource "aws_iam_role_policy_attachment" "extract_data_kinesis" {
  role       = aws_iam_role.extract_data_role.name
  policy_arn = aws_iam_policy.extract_kinesis_policy.arn
}