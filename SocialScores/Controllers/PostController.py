from fastapi import APIRouter, Depends
from SocialScores.Models.Post import PostBase
from SocialScores.Controllers import PostController
from SocialScores.Database.DatabaseFactory import DatabaseFactory

DATABASE_ENGINE = 'postgres'
CONNECTION_STRING = 'dbname=socialscores user=postgres password=admin host=database port=5432'

router = APIRouter()

# Dependency to provide a connected database
def get_database():
    db_factory = DatabaseFactory()
    database = db_factory.create(DATABASE_ENGINE, CONNECTION_STRING)
    database.connect()
    try:
        yield database
    finally:
        database.close()

@router.post("/api/v1/post")
async def create_post(post: PostBase, database=Depends(get_database)):
    response = PostController.create_post(post, database)
    return response

@router.get("/api/v1/post/{post_id}")
async def get_post(post_id: int, database=Depends(get_database)):
    response = PostController.get_post(post_id, database)
    return response

@router.get("/api/v1/post/latest")
async def get_post_latest(database=Depends(get_database)):
    response = PostController.get_post_latest(database)
    return response

@router.get("/api/v1/post/search/{query}")
async def search_post(query: str, database=Depends(get_database)):
    response = PostController.search_post(query, database)
    return response
