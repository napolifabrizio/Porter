import bcrypt


def verify_password(db, raw_password) -> bool:
    stored_hash = db.get_config("password_hash")
    if stored_hash is None:
        return False
    return bcrypt.checkpw(raw_password.encode(), stored_hash.encode())
