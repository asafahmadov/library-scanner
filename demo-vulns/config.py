"""Hardcoded secrets (secrets-scan demo target).

All values are DUMMIES — AWS's public EXAMPLE keys and obvious fakes. Not real.
"""
# CWE-798: hardcoded credentials.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "SuperSecret123!"
GITHUB_TOKEN = "ghp_FAKE0000000000000000000000000000000000"

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA1234FAKEDEMOKEYDONOTUSEabcdefghijklmnopqrstuvwxyz00
-----END RSA PRIVATE KEY-----"""
