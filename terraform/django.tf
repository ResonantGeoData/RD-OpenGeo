data "heroku_team" "this" {
  name = "kitware"
}

resource "aws_route53_zone" "this" {
  name = "resonantgeodata.com"
}

module "django" {
  source  = "girder/django/heroku"
  version = "0.9.2"

  project_slug     = "rd-opengeo"
  subdomain_name   = "www"
  heroku_team_name = data.heroku_team.this.name
  route53_zone_id  = aws_route53_zone.this.id

  # Optional overrides
  # See https://registry.terraform.io/modules/girder/django/heroku/
  # for other possible optional variables
  additional_django_vars = {
    DJANGO_SENTRY_DSN = "https://b3dac135af6c42fea439998200656ca3@o267860.ingest.sentry.io/5458973"
  }
  # This defaults to 1, but may be changed
  heroku_worker_dyno_quantity = 0
  heroku_web_dyno_size        = "standard-2x"
  heroku_worker_dyno_size     = "standard-1x"
  heroku_postgresql_plan      = "hobby-basic"
}
