# app/security/lock.py
import hashlib, os

def initialize():
    expected_hash = os.environ.get("INIT_HASH")
    if not expected_hash:
        raise SystemExit("Missing INIT_HASH.")

    file_path = os.path.abspath("app/__init__.py")
    with open(file_path, 'rb') as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != expected_hash:
        raise SystemExit("Tampering detected. This is the day you will always remember as the day you almost stole our code.")
