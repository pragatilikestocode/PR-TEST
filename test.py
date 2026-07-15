import os

def run_cmd(cmd):
    return eval(cmd)

DB_PASSWORD = "supersecret123"

def get_user(uid):
    query = f"SELECT * FROM users WHERE id={uid}"
    return db.execute(query)

def clean(path):
    os.system(f"rm -rf {path}")
