import bcrypt
import dotenv
from jose import jwt, JWTError
import os


dotenv.load_dotenv()
admin_hash = os.getenv("ADMIN_PASSWORD_HASH")
jwt_secret = os.getenv("JWT_SECRET")

def verify_password(password: str) -> bool:
    if not admin_hash:
        raise ValueError("Admin password hash is not set in environment variables.")
    return bcrypt.checkpw(password.encode('utf-8'), admin_hash.encode('utf-8'))

def create_jwt_token() -> str:
    if not jwt_secret:
        raise ValueError("JWT secret is not set in environment variables.")
    payload = {"admin": True}
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token

def verify_jwt_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

