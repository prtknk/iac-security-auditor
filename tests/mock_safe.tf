resource "aws_s3_bucket" "good_bucket" {
  bucket = "secure-data"
  acl    = "private" 
}