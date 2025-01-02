from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Database.Database import get_db

class ImageController:
    def __init__(self, db: Session):
        self.repo = RepositoryImage(db)

    def add_image(self, filename: str, file_path: str, uploader: str):
        return self.repo.add_image(filename=filename, file_path=file_path, uploader=uploader)

    def get_image_by_id(self, image_id: int):
        image = self.repo.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    def search_images(self, query: str):
        results = self.repo.search_images(query)
        if not results:
            raise HTTPException(status_code=404, detail="No images found")
        return results

router = APIRouter()

@router.post("/")
def create_image(filename: str, file_path: str, uploader: str, db: Session = Depends(get_db)):
    controller = ImageController(db)
    return controller.add_image(filename=filename, file_path=file_path, uploader=uploader)

@router.get("/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    controller = ImageController(db)
    return controller.get_image_by_id(image_id)

@router.get("/action/search/")
def search_images(query: str, db: Session = Depends(get_db)):
    controller = ImageController(db)
    return controller.search_images(query)