resource "aws_sqs_queue" "dead_letters" {
  name = "${var.environment}-dead-letters"
}