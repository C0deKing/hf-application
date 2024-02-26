resource "aws_ecr_repository" "lambda_base" {
  name = "${var.environment}-lambda-base-image"


  image_scanning_configuration {
    scan_on_push = true
  }
}


data "external" "project_version" {
  program = ["bash", "${path.module}/version.sh"]
}

resource "null_resource" "docker_packaging" {


  provisioner "local-exec" {
    command = <<EOF
        cd ..
	    aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com
	    gradle build -p noiselesstech
	    docker build -t "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}" -f Dockerfile .
	    docker push "${aws_ecr_repository.lambda_base.repository_url}:${data.external.project_version.result.version}"
	    EOF
  }


  triggers = {
    "version_change" = data.external.project_version.result.version
  }


  depends_on = [
    aws_ecr_repository.lambda_base,
  ]
}