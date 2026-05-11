from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta, timezone
import os

pwd_context=CryptContext(schemes=["bcrypt"])

SECRET_KEY=os.getenv("SECRET_KEY")

def hash_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data):
    to_encode=data.copy()
    expiry=datetime.now(timezone.utc)+ timedelta(minutes=30)
    to_encode["exp"]=expiry 
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

