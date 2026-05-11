from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token

router=APIRouter()

@router.post("/register")
def register(email, password, db: Session=Depends(get_db)):
    result=db.query(User).filter(User.email==email).first()
    if result is not    None:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        new_user=User(email=email, hashed_password=hash_password(password))
        db.add(new_user)
        db.commit()
        return {"message" : "user registered successfully"}
        
@router.post("/login")
def login(email, password, db: Session=Depends(get_db)):
    user=db.query(User).filter(User.email==email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return create_access_token({"sub":str(user.id)})

