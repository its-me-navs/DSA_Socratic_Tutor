from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.chats import router as chat_router
from database import engine
from models import Base

app=FastAPI()

@app.get("/")
def root():
    return {"Message" : "DSA Chatbot API running"}

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router)

Base.metadata.create_all(bind=engine)