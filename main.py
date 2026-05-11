from fastapi import FastAPI
from routes.auth import router as auth_router
from database import engine
from models import Base

app=FastAPI()

@app.get("/")
def root():
    return {"Message" : "DSA Chatbot API running"}

app.include_router(auth_router, prefix="/auth")

Base.metadata.create_all(bind=engine)