"""Intentionally vulnerable Flask app — academic / KillLoop lab only."""
import os
import sqlite3

from flask import Flask, jsonify, request

from app.config import load_settings
from app.shell_util import run_unsafe_command

app = Flask(__name__)
SETTINGS = load_settings()


def init_db():
    conn = sqlite3.connect("/tmp/users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, name TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users VALUES ('1', 'alice')")
    conn.commit()
    conn.close()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "variant": "vulnerable", "app": SETTINGS["app_name"]})


@app.get("/user")
def get_user():
    """Runtime SQLi — canary hits this with ?id=1' OR '1'='1"""
    user_id = request.args.get("id", "")
    conn = sqlite3.connect("/tmp/users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"exploit_blocked": False, "user": {"id": row[0], "name": row[1]}})
    return jsonify({"exploit_blocked": False, "user": None}), 404


@app.post("/admin/run")
def admin_run():
    """Command injection surface for SAST (Bandit/Semgrep)."""
    filename = request.json.get("file", "readme.txt") if request.is_json else "readme.txt"
    output = run_unsafe_command(filename)
    return jsonify({"output": output})


init_db()
