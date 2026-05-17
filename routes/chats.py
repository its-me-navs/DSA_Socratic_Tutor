from auth import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from models import ChatSession, Message
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import os
from groq import Groq

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

router=APIRouter()

class SessionCreate(BaseModel):
    title: str

class UserMessage(BaseModel):
    content: str

@router.post("/chat/session")
def new_session(body: SessionCreate, user_id: int=Depends(get_current_user), db: Session=Depends(get_db)):
    newsession=ChatSession(title=body.title, user_id=user_id)
    db.add(newsession)
    db.commit()
    db.refresh(newsession)
    return {"session_id":newsession.id, "title":newsession.title}

@router.post("/chat/session/{session_id}/message")
def messages(session_id: int, user_message: UserMessage, user_id: int=Depends(get_current_user), db: Session=Depends(get_db)):
    session=db.query(ChatSession).filter(ChatSession.id==session_id, ChatSession.user_id==user_id).first()
    if not session:
        raise HTTPException(status_code=403, detail="unauthorized")
    message=user_message.content
    message_history=db.query(Message).filter(Message.session_id==session_id).all()
    history = [
        {"role": msg.role if msg.role == "user" else "assistant", "content": msg.content}
        for msg in message_history]
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=history)
    new_messages=[
        Message(session_id=session_id, role="user", content=message),
        Message(session_id=session_id, role="model", content=response.choices[0].message.content)]
    db.add_all(new_messages)
    db.commit()
    return {"response":response.choices[0].message.content}

@router.get("/chat/session/{session_id}/history")
def history(session_id:int, user_id: int=Depends(get_current_user), db: Session=Depends(get_db)):
    session=db.query(ChatSession).filter(ChatSession.user_id==user_id, ChatSession.id==session_id).first()
    if not session:
        raise HTTPException(status_code=403, detail="unauthorized")
    chat_history=db.query(Message).filter(Message.session_id==session_id).all()
    return chat_history