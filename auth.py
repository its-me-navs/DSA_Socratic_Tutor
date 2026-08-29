from passlib.context import CryptContext
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
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

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="user not found")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
    
    user=db.query(User).filter(User.id==int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    return user