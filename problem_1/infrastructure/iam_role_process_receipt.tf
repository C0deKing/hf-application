resource "aws_iam_role" "process_receipt_role" {
  name               = "${var.environment}-process-receipt-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_role_policy_attachment" "process_receipt_application_access" {
  role       = aws_iam_role.process_receipt_role.name
  policy_arn = aws_iam_policy.application_iam_policy.arn
}

resource "aws_iam_role_policy_attachment" "process_receipt_kinesis" {
  role       = aws_iam_role.process_receipt_role.name
  policy_arn = aws_iam_policy.process_kinesis_policy.arn
}