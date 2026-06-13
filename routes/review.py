from auth import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from models import ReviewItem, User
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

router = APIRouter()

REVIEW_INTERVALS = [1, 2, 5, 10, 25]  # days

class ReviewCreate(BaseModel):
    problem: str

@router.post("/review/add")
def add_review(body: ReviewCreate, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    item = ReviewItem(user_id=user.id, problem=body.problem, stage=0, next_review=datetime.now(timezone.utc))
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "problem": item.problem, "next_review": item.next_review}

@router.get("/review/due")
def due_reviews(user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    now = datetime.now(timezone.utc)
    items = db.query(ReviewItem).filter(ReviewItem.user_id==user.id, ReviewItem.next_review<=now).all()
    return [{"id": i.id, "problem": i.problem, "stage": i.stage, "next_review": i.next_review} for i in items]

@router.post("/review/{item_id}/complete")
def complete_review(item_id: int, user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    item = db.query(ReviewItem).filter(ReviewItem.id==item_id, ReviewItem.user_id==user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    if item.stage < len(REVIEW_INTERVALS) - 1:
        item.stage += 1
    days = REVIEW_INTERVALS[item.stage]
    item.next_review = datetime.now(timezone.utc) + timedelta(days=days)
    db.commit()
    return {"id": item.id, "stage": item.stage, "next_review": item.next_review}