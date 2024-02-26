resource "aws_iam_policy" "dead_letter_sqs_policy" {

  name        = "${var.environment}-dead-letter-sqs-policy"
  path        = "/"
  description = "AWS IAM Policy for the receipt extraction dead letter processor"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
        "sqs:GetQueueAttributes",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage"
     ],
     "Resource": "${aws_sqs_queue.dead_letters.arn}",
     "Effect": "Allow"
   }
 ]
}
EOF
}