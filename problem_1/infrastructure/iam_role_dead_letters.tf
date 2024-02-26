resource "aws_iam_role" "dead_letter_role" {
  name               = "${var.environment}-dead-letter-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_role_policy_attachment" "dead_letter_application_access" {
  role       = aws_iam_role.dead_letter_role.name
  policy_arn = aws_iam_policy.application_iam_policy.arn
}

resource "aws_iam_role_policy_attachment" "dead_letter_sqs" {
  role       = aws_iam_role.dead_letter_role.name
  policy_arn = aws_iam_policy.dead_letter_sqs_policy.arn
}