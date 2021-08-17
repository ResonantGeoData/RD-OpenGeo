# Apex domains on Route 53 do not support CNAME records. So, follow the general suggestion
# from https://devcenter.heroku.com/articles/route-53#naked-root-domain to use S3 to issue a
# redirect. Use CloudFront too, to allow connections from HTTPS.

locals {
  redirect_apex_from_domain = aws_route53_zone.this.name # apex domain
  redirect_apex_to_domain   = module.django.fqdn
}

module "redirect_apex_s3" {
  source  = "cloudposse/cloudfront-s3-cdn/aws"
  version = "0.74.0"

  namespace = "rd-opengeo"
  name      = "redirect-apex"

  aliases             = [local.redirect_apex_from_domain]
  dns_alias_enabled   = true
  parent_zone_id      = aws_route53_zone.this.id
  acm_certificate_arn = module.redirect_apex_acm.arn

  website_enabled = true
  # Force all requests to go through CloudFront
  s3_website_password_enabled = true
  # Ensure HTTPS
  redirect_all_requests_to = "https://${local.redirect_apex_to_domain}"
  default_root_object      = null

  cloudfront_access_logging_enabled = false
  versioning_enabled                = false
}

module "redirect_apex_acm" {
  source  = "cloudposse/acm-request-certificate/aws"
  version = "0.14.0"

  domain_name = local.redirect_apex_from_domain
}
