# Hardened infrastructure — apPosture auto-fix.

variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_security_group" "app" {
  name = "demo-restricted"

  ingress {
    description = "App port from the VPC only (was 0-65535 from 0.0.0.0/0)"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "apposture-demo-private-bucket"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_db_instance" "db" {
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  publicly_accessible = false
  storage_encrypted   = true
  username            = "admin"
  password            = var.db_password
  skip_final_snapshot = true
}
