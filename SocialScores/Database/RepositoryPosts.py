from SocialScores.Models.Post import Post, PostBase, PostResponse
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime

table_name = "posts"

columns = {
    "id": "SERIAL PRIMARY KEY",
    '"user"': "TEXT NOT NULL",
    "text": "TEXT",
    "image": "TEXT",
    "time_created": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
}

class RepositoryPosts:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user: str, account_id: int, text: str, image_id: Optional[int] = None):
        new_post = Post(user=user, account_id=account_id, text=text, image_id=image_id)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)

        return new_post

    def get_post_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_latest_posts(self, limit: int = 10):
        return self.db.query(Post).options(joinedload(Post.image)).order_by(Post.time_created.desc()).limit(limit).all()

    def search_posts(self, query: str):
        return self.db.query(Post).options(joinedload(Post.image)).filter(Post.text.ilike(f"%{query}%")).all()

    def get_posts_by_account_id(self, account_id: int):
        return self.db.query(Post).options(joinedload(Post.image)).filter(Post.account_id == account_id).all()
