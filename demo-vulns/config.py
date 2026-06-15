"""Secrets loaded from the environment — hardened by apPosture auto-fix.

CWE-798 fixed: no hardcoded credentials; load from the environment / a secrets
manager at runtime. Set these as masked CI / deployment variables.
"""
import os

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "")
