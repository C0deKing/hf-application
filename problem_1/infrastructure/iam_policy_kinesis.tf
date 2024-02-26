resource "aws_iam_policy" "api_kinesis_policy" {

  name        = "${var.environment}-api-lambda-kinesis-policy"
  path        = "/"
  description = "AWS IAM Policy for the receipt extraction API service"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
        "kinesis:PutRecord"
     ],
     "Resource": "${aws_kinesis_stream.process_receipt_stream.arn}",
     "Effect": "Allow"
   }
 ]
}
EOF
}

resource "aws_iam_policy" "process_kinesis_policy" {

  name        = "${var.environment}-process-receipt-lambda-kinesis-policy"
  path        = "/"
  description = "AWS IAM Policy for the receipt extraction API service"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
        "kinesis:DescribeStream",
        "kinesis:DescribeStreamSummary",
        "kinesis:GetRecords",
        "kinesis:GetShardIterator",
        "kinesis:ListShards",
        "kinesis:ListStreams",
        "kinesis:SubscribeToShard"
     ],
     "Resource": "${aws_kinesis_stream.process_receipt_stream.arn}",
     "Effect": "Allow"
   },
   {
     "Action": [
        "kinesis:ListStreams"
     ],
     "Resource": "*",
     "Effect": "Allow"
   },
   {
     "Action": [
        "kinesis:PutRecord"
     ],
     "Resource": [
        "${aws_kinesis_stream.extract_data_stream.arn}"
     ],
     "Effect": "Allow"
   },
   {
     "Action": [
        "sqs:SendMessage"
     ],
     "Resource": [
        "${aws_sqs_queue.dead_letters.arn}"
     ],
     "Effect": "Allow"
   }
 ]
}
EOF
}


resource "aws_iam_policy" "extract_kinesis_policy" {

  name        = "${var.environment}-extract-kinesis-policy"
  path        = "/"
  description = "AWS IAM Policy for the receipt extraction API service"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
        "kinesis:DescribeStream",
        "kinesis:DescribeStreamSummary",
        "kinesis:GetRecords",
        "kinesis:GetShardIterator",
        "kinesis:ListShards",
        "kinesis:ListStreams",
        "kinesis:SubscribeToShard"
     ],
     "Resource": "${aws_kinesis_stream.extract_data_stream.arn}",
     "Effect": "Allow"
   },
   {
     "Action": [
        "sqs:SendMessage"
     ],
     "Resource": [
        "${aws_sqs_queue.dead_letters.arn}"
     ],
     "Effect": "Allow"
   }
 ]
}
EOF
}

