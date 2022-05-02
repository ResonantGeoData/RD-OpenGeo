provider "aws" {
  alias               = "aws_ohio"
  region              = "us-east-2"
  allowed_account_ids = ["381864640041"]
  # Must set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY envvars
}
