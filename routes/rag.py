from auth import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from models import EmbeddingItem, User
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from embeddings import get_embedding, cosine_similarity
import json

router = APIRouter()

class EmbedCreate(BaseModel):
    content: str
    source_type: str = "problem"

@router.post("/rag/add")
def add_embedding(body: EmbedCreate, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    vec = get_embedding(body.content)
    item = EmbeddingItem(user_id=user.id, content=body.content, embedding=vec, source_type=body.source_type)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "content": item.content}

@router.get("/rag/search")
def search_embeddings(query: str, top_k: int = 3, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    query_vec = json.loads(get_embedding(query))
    items = db.query(EmbeddingItem).filter(EmbeddingItem.user_id==user.id).all()

    scored = []
    for item in items:
        item_vec = json.loads(item.embedding)
        score = cosine_similarity(query_vec, item_vec)
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]
    return [{"id": item.id, "content": item.content, "score": score} for score, item in top]