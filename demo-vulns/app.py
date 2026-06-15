"""Flask app — hardened by apPosture auto-fix."""
import hashlib
import json
import sqlite3
import subprocess

import yaml
from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    uid = request.args.get("id", "")
    conn = sqlite3.connect("app.db")
    # CWE-89 fixed: parameterized query, no string concatenation.
    return str(conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # CWE-78 fixed: argument array (no shell) + input validation.
    if not host.replace(".", "").replace("-", "").isalnum():
        return "invalid host", 400
    return subprocess.check_output(["ping", "-c", "1", host])


@app.route("/load")
def load():
    data = request.args.get("data", "")
    # CWE-502 fixed: JSON instead of pickle — no code execution.
    return str(json.loads(data))


def weak_hash(password: str) -> str:
    # CWE-327 fixed: SHA-256 (use bcrypt/argon2 as a KDF for real passwords).
    return hashlib.sha256(password.encode()).hexdigest()


def load_config(text: str):
    # CWE-20 fixed: safe_load — no arbitrary tags.
    return yaml.safe_load(text)


if __name__ == "__main__":
    # CWE-489 fixed: bound to loopback, debug off.
    app.run(host="127.0.0.1", debug=False)
