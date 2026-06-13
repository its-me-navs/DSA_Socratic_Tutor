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
    sessions=relationship("ChatSession", back_populates="user")

class ChatSession(Base):
    __tablename__="chatsessions"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    mode=Column(String, default="practice")
    title=Column(String, nullable=False)
    problem=Column(String, nullable=True)
    created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user=relationship("User", back_populates="sessions")
    messages=relationship("Message", back_populates="session")

class Message(Base):
    __tablename__="messages"
    id=Column(Integer, primary_key=True)
    session_id=Column(Integer, ForeignKey("chatsessions.id"))
    role=Column(String, nullable=False)
    content=Column(String)
    created_at=Column(DateTime, default=lambda:datetime.now(timezone.utc))
    session=relationship("ChatSession", back_populates="messages")

class ReviewItem(Base):
    __tablename="reviewitems"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    problem=Column(String, nullable=False)
    stage=Column(Integer, default=0)
    next_review=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at=Column(DateTime, default=lambda: datetime.now(timezone.utc))