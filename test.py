from database import SessionLocal
from models import EmbeddingItem
db = SessionLocal()
for item in db.query(EmbeddingItem).all():
    print(item.id, item.user_id, item.content)