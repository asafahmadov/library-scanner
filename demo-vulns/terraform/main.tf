# Intentionally insecure infrastructure (IaC demo target).

resource "aws_security_group" "open" {
  name = "demo-open"

  ingress {
    description = "Open to the entire internet"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "public" {
  bucket = "apposture-demo-public-bucket"
  acl    = "public-read"
}

# Encryption intentionally omitted on the bucket above.

resource "aws_db_instance" "db" {
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  publicly_accessible    = true
  storage_encrypted      = false
  username               = "admin"
  password               = "SuperSecret123!"
  skip_final_snapshot    = true
}
