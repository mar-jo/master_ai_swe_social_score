from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from SocialScores.Models.post import PostCreate, PostResponse
from SocialScores.Database.DatabaseFactory import DatabaseFactory
from SocialScores.Database.RepositoryPosts import RepositoryPosts

from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
factory = DatabaseFactory()

db = factory.create(
    type="postgresql",
    db_name=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT"))
)

try:
    db.connect()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    raise

repo = RepositoryPosts(db)

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    repo.add_post(post)
    return post

@router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int):
    post = repo.get_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
