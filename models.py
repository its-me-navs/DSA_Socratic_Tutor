from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    email=Column(String, unique=True)
    hashed_password=Column(String, nullable=False)
    created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ChatSession(Base):
    __tablename__="chatsessions"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Message(Base):
    __tablename__="messages"
    id=Column(Integer, primary_key=True)
    session_id=Column(Integer, ForeignKey("chatsessions.id"))
    role=Column(String, nullable=False)
    content=Column(String)
    created_at=Column(DateTime, default=lambda:datetime.now(timezone.utc))

