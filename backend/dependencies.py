import jwt, os, httpx
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash

def hash_password(password):

    password_hash = PasswordHash.recommended()

    return password_hash.hash(password)

def verify_password(hashed_password, password):
    password_hash = PasswordHash.recommended()

    return password_hash.verify(password, hashed_password)

def authenticate_user(user, password) -> bool:
    return verify_password(user["hashed_password"], password)

def generate_token(email):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(payload=to_encode, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt
    
def verify_token(token) -> str:
    try:
        data = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = data.get("sub")
        if not email:
            return None
    except InvalidTokenError:
        return None

    return email

def check_bookings():
    httpx.get("http://server:8000/api/bookings")