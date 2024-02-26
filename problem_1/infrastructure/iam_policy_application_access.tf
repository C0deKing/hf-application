resource "aws_iam_policy" "application_iam_policy" {

  name        = "${var.environment}-application-access-role"
  path        = "/"
  description = "AWS IAM Policy for the receipt extraction application services"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   },
   {
     "Action": [
       "dynamodb:Get*",
       "dynamodb:PutItem"
     ],
     "Resource": "${aws_dynamodb_table.receipt-data.arn}",
     "Effect": "Allow"
   },
   {
     "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:DeleteObject"
     ],
     "Resource": "${aws_s3_bucket.receipt_data.arn}/*",
     "Effect": "Allow"
   },
   {
     "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:AssignPrivateIpAddresses",
        "ec2:UnassignPrivateIpAddresses"
     ],
     "Resource": "*",
     "Effect": "Allow"
   }
 ]
}
EOF
}