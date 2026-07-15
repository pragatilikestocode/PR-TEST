import os
import subprocess
import random
import secrets
import sqlite3

DB_PASSWORD = "supersecret123"          # Hardcoded secret
API_KEY = "sk-test-abcdef123456"        # Hardcoded secret


# --------------------------
# HIGH RISK
# --------------------------

def run_user_code(user_input):
    # Dangerous: executes arbitrary Python
    return eval(user_input)


def execute_shell(command):
    # Dangerous: shell injection
    return subprocess.run(command, shell=True)


def cleanup(path):
    # Dangerous: command injection
    os.system(f"rm -rf {path}")


def fetch_user(conn, uid):
    # Dangerous: SQL injection
    query = f"SELECT * FROM users WHERE id={uid}"
    return conn.execute(query).fetchall()


# --------------------------
# CONTEXT-DEPENDENT
# --------------------------

def safe_math():
    # Looks scary to static analysis, but is constant and not user-controlled.
    expression = "2 + 2"
    return eval(expression)


def trusted_admin_task():
    # Runs a fixed command, no user input involved.
    return subprocess.run(["git", "--version"], check=True)


def cleanup_temp():
    # Fixed command, not user-controlled.
    os.system("echo Cleaning temporary directory")


def fetch_fixed_user(conn):
    # Constant SQL string.
    query = "SELECT * FROM users WHERE id=1"
    return conn.execute(query).fetchall()


# --------------------------
# SAFE IMPLEMENTATIONS
# --------------------------

def safe_fetch_user(conn, uid):
    return conn.execute(
        "SELECT * FROM users WHERE id=?",
        (uid,),
    ).fetchall()


def generate_token():
    return secrets.token_hex(32)


def secure_random():
    return secrets.randbelow(100)


# --------------------------
# LOW RISK / CODE QUALITY
# --------------------------

def debug_login(username):
    print(f"Authenticating {username}")     # Debug print


def lottery():
    # Not security-sensitive. random is acceptable here.
    return random.randint(1, 100)


def choose_color():
    colors = ["red", "green", "blue"]
    return random.choice(colors)


# --------------------------
# SHOULD NOT BE FLAGGED
# --------------------------

def calculate_area(radius):
    return 3.14159 * radius * radius


def greet(name):
    return f"Hello, {name}"


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    print(greet("Alice"))
