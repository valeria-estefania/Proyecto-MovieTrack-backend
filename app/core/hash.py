import bcrypt

def hashear_password(password: str) -> str:
    password_bytes = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verificar_password(password: str, hashed: str) -> bool:
    password_bytes = password[:72].encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)