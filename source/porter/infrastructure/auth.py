import bcrypt


def verify_password(stored_hash: str, raw_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode(), stored_hash.encode())
