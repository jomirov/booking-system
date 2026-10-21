import jwt, os
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
from httpx import AsyncClient

def hash_password(password):

    password_hash = PasswordHash.recommended()

    return password_hash.hash(password)

def verify_password(hashed_password, password):
    password_hash = PasswordHash.recommended()

    return password_hash.verify(password, hashed_password)

def authenticate_user(user, password) -> bool:
    return verify_password(user["hashed_password"], password)

def generate_token(user_id, user_email):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
    to_encode = {"sub": user_email, "user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(payload=to_encode, key=os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt
    
def verify_token(token) -> dict:
    data = jwt.decode(jwt=token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    email = data.get("sub")
    id = data.get("user_id")
    if not email:
        raise InvalidTokenError
    return {"id": id, "email": email}

async def check_expired_bookings():
    async with AsyncClient() as client:
        await client.put(url="http://server:8000/api/bookings/expired")