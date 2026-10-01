import jwt, os, pwdlib
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import httpx


load_dotenv()
password_hash = pwdlib.PasswordHash.recommended()
def hash_password(password):
    return password_hash.hash(password=password)

def validate_date(strdate: str):
    format = "%Y-%m-%d"
    dtime = datetime.strptime(strdate, format).replace(tzinfo=timezone.utc).timestamp()
    current_time = datetime.now(tz=timezone.utc).timestamp()

    if dtime > current_time:
        return True
    return False

def check_expired_bookings():
    res = httpx.get("http://server:8000/api/bookings")
    bookings = res.json()
    
    for booking in bookings:
        if datetime.now(timezone.utc).timestamp() > datetime.strptime(booking["expires_at"], "%Y-%m-%d %H:%M:%S").timestamp():
            httpx.put(f"http://server:8000/api/bookings/{booking["id"]}", content="EXPIRED")