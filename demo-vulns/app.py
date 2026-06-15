"""Intentionally vulnerable Flask app (SAST demo target)."""
import hashlib
import pickle
import sqlite3
import subprocess

import yaml
from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def get_user():
    uid = request.args.get("id")
    conn = sqlite3.connect("app.db")
    # CWE-89: SQL injection — untrusted input concatenated into the query.
    query = "SELECT * FROM users WHERE id = '" + uid + "'"
    return str(conn.execute(query).fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")
    # CWE-78: OS command injection — untrusted input into a shell.
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/load")
def load():
    data = request.args.get("data")
    # CWE-502: insecure deserialization of untrusted data.
    return str(pickle.loads(bytes.fromhex(data)))


def weak_hash(password: str) -> str:
    # CWE-327: weak hashing algorithm.
    return hashlib.md5(password.encode()).hexdigest()


def load_config(text: str):
    # CWE-20: unsafe YAML load executes arbitrary tags.
    return yaml.load(text)


if __name__ == "__main__":
    # CWE-489: debug server bound to all interfaces.
    app.run(host="0.0.0.0", debug=True)
