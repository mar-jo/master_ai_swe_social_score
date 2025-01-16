from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryPosts import RepositoryPosts
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Controllers.ImageController import ImageController
from typing import Optional
import base64
from SocialScores.Models.Post import PostBase
from SocialScores.Database.Database import get_db
from SocialScores.Services.TextGenerationService import TextGenerationService

class PostController:
    def __init__(self, db):
        self.repo = RepositoryPosts(db)
        self.image_repo = RepositoryImage(db)

    def create_post(self, user: str, account_id: int, text: str, image: Optional[UploadFile] = None):
        if image:
            binary_data = image.file.read()
            new_image = self.image_repo.add_image(
                filename=image.filename,
                binary_data=binary_data,
                uploader=user
            )
            image_id = new_image.id

            ImageController.send_resize_request(image_id)
        else:
            image_id = None

        new_post = self.repo.create_post(
            user=user,
            account_id=account_id,
            text=text,
            image_id=image_id
        )
        return new_post

    def get_post(self, post_id: int, resized: bool = False):
        post = self.repo.get_post_by_id(post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return {
            "id": post.id,
            "user": post.user,
            "account_id": post.account_id,
            "text": post.text,
            "time_created": post.time_created,
            "image": {
                "filename": post.image.filename,
                "data": base64.b64encode(
                    post.image.resized_binary_data if resized else post.image.binary_data
                ).decode("utf-8"),
                "uploader": post.image.uploader,
                "time_created": post.image.time_created,
            } if post.image else None,
        }

    def get_latest_posts(self, limit: int = 10, resized: bool = False):
        posts = self.repo.get_latest_posts(limit)
        return [
            {
                "id": post.id,
                "user": post.user,
                "account_id": post.account_id,
                "text": post.text,
                "time_created": post.time_created,
                "image": {
                    "filename": post.image.filename,
                    "data": base64.b64encode(
                        post.image.resized_binary_data if resized else post.image.binary_data
                    ).decode("utf-8"),
                    "uploader": post.image.uploader,
                    "time_created": post.image.time_created,
                } if post.image else None,
            }
            for post in posts
        ]

    def search_posts(self, query: str, resized: bool = False):
        posts = self.repo.search_posts(query)
        return [
            {
                "id": post.id,
                "user": post.user,
                "account_id": post.account_id,
                "text": post.text,
                "time_created": post.time_created,
                "image": {
                    "filename": post.image.filename,
                    "data": base64.b64encode(
                        post.image.resized_binary_data if resized else post.image.binary_data
                    ).decode("utf-8"),
                    "uploader": post.image.uploader,
                    "time_created": post.image.time_created,
                } if post.image else None,
            }
            for post in posts
        ]

    def get_posts_for_account(self, account_id: int):
        posts = self.repo.get_posts_by_account_id(account_id)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this account")
        return [
            {
                "id": post.id,
                "user": post.user,
                "account_id": post.account_id,
                "text": post.text,
                "time_created": post.time_created,
                "image": {
                    "filename": post.image.filename,
                    "data": base64.b64encode(post.image.binary_data).decode("utf-8"),
                    "uploader": post.image.uploader,
                    "time_created": post.image.time_created,
                } if post.image else None,
            }
            for post in posts
        ]

router = APIRouter()
text_gen_service = TextGenerationService()

@router.post("/")
def create_post(user: str = Form(...), account_id: int = Form(...), text: str = Form(None), image: UploadFile = File(None), db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.create_post(user=user, account_id=account_id, text=text, image=image)

@router.get("/action/search/")
async def search_posts(query: str, resized: bool = Query(False), db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.search_posts(query, resized=resized)

@router.get("/action/latest/")
async def get_latest_posts(limit: int = 10, resized: bool = Query(False), db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.get_latest_posts(limit=limit, resized=resized)

@router.get("/{post_id}")
async def get_post(post_id: int, resized: bool = Query(False), db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.get_post(post_id, resized=resized)

@router.post("/generate")
def generate_post(account_id: int, user: str, prompt: str, image: UploadFile = File(None), db: Session = Depends(get_db)):
    controller = PostController(db)
    generated_text = text_gen_service.generate_text(prompt)
    if not generated_text:
        raise HTTPException(status_code=500, detail="Failed to generate text.")
    new_post = controller.create_post(user=user, account_id=account_id, text=generated_text, image=image)
    return {"message": "Post created with generated content", "post": new_post}