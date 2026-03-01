resource "aws_s3_bucket" "my_company_data" {
  bucket = "sensitive-customer-data-bucket"
  acl    = "public-read" 
}

# NEW: Security Group with an open SSH port
resource "aws_security_group" "web_server_sg" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Vulnerability: Open to the world
  }
}

# NEW: RDS Database without storage encryption
resource "aws_db_instance" "default" {
  allocated_storage    = 10
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"
  storage_encrypted    = false # Vulnerability: Unencrypted data at rest
}