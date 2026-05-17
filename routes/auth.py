from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")   
def register(body: RegisterRequest, db: Session=Depends(get_db)):
    result=db.query(User).filter(User.email==body.email).first()
    if result is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        new_user=User(email=body.email, hashed_password=hash_password(body.password))
        db.add(new_user)
        db.commit()
        return {"message" : "user registered successfully"}
        
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):    
    user=db.query(User).filter(User.email==form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"access_token": create_access_token({"sub":str(user.id)}), "token_type":"bearer"}