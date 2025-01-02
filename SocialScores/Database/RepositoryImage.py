from sqlalchemy.orm import Session
from typing import List, Optional
from SocialScores.Models.Image import Image
from sqlalchemy import desc

class RepositoryImage:
    def __init__(self, db: Session):
        self.db = db

    def add_image(self, filename: str, file_path: str, uploader: str):
        new_image = Image(filename=filename, file_path=file_path, uploader=uploader)
        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)

        return new_image

    def get_image_by_id(self, image_id: int) -> Optional[Image]:
        return self.db.query(Image).filter(Image.id == image_id).first()

    def search_images(self, query: str) -> List[Image]:
        return (
            self.db.query(Image)
            .filter(
                (Image.filename.ilike(f"%{query}%")) | (Image.uploader.ilike(f"%{query}%"))
            )
            .all()
        )
