import bcrypt
    
def get_password_hash(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)