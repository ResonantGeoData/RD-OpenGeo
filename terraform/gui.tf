resource "aws_route53_record" "gui" {
  zone_id = aws_route53_zone.this.zone_id
  name    = "gui"
  type    = "CNAME"
  ttl     = "300"
  records = ["rgd-vue.netlify.app."]
}
