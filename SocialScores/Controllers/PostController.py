from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryPosts import RepositoryPosts
from SocialScores.Models.Post import PostBase, PostResponse
from SocialScores.Database.Database import get_db

class PostController:
    def __init__(self, db):
        self.repo = RepositoryPosts(db)

    def create_post(self, post_data: PostBase):
        return self.repo.create_post(
            user=post_data.user,
            text=post_data.text,
            image=post_data.image
        )

    def get_post(self, post_id: int):
        return self.repo.get_post_by_id(post_id)

    def get_latest_posts(self, limit: int = 10):
        return self.repo.get_latest_posts(limit)

    def search_posts(self, query: str):
        return self.repo.search_posts(query)

router = APIRouter()

@router.post("/")
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.create_post(post)

@router.get("/action/search/")
async def search_posts(query: str, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.search_posts(query)

@router.get("/action/latest/")
async def get_latest_posts(limit: int = 10, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.get_latest_posts(limit)

@router.get("/{post_id}")
async def get_post(post_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    post = controller.get_post(post_id)
    if not post:
        return {"detail": "Post not found"}
    return post

