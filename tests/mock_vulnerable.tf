resource "aws_s3_bucket" "bad_bucket" {
  bucket = "exposed-data"
  acl    = "public-read" 
}