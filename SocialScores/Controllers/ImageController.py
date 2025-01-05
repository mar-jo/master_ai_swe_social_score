from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Models.Image import ImageBase, ImageResponse
from SocialScores.Database.Database import get_db
from typing import List

class ImageController:
    def __init__(self, db: Session):
        self.repo = RepositoryImage(db)

    def add_image(self, filename: str, binary_data: bytes, uploader: str):
        return self.repo.add_image(filename=filename, binary_data=binary_data, uploader=uploader)

    def get_image_by_id(self, image_id: int):
        image = self.repo.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    def get_latest_images(self, limit: int = 10):
        return self.repo.get_latest_images(limit)

router = APIRouter()

@router.post("/upload", response_model=ImageResponse)
def upload_image(uploader: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    controller = ImageController(db)
    binary_data = file.file.read()
    return controller.add_image(filename=file.filename, binary_data=binary_data, uploader=uploader)

@router.get("/{image_id}", response_model=ImageResponse)
def get_image(image_id: int, db: Session = Depends(get_db)):
    controller = ImageController(db)
    return controller.get_image_by_id(image_id)

@router.get("/latest", response_model=List[ImageResponse])
def get_latest_images(limit: int = 10, db: Session = Depends(get_db)):
    controller = ImageController(db)
    return controller.get_latest_images(limit)