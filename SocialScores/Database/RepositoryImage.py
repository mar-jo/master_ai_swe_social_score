from sqlalchemy.orm import Session
from SocialScores.Models.Image import Image

class RepositoryImage:
    def __init__(self, db: Session):
        self.db = db

    def add_image(self, filename: str, binary_data: bytes, uploader: str):
        new_image = Image(filename=filename, binary_data=binary_data, uploader=uploader)
        self.db.add(new_image)
        self.db.commit()
        self.db.refresh(new_image)

        return new_image

    def add_resized_image(self, image_id: int, resized_binary_data: bytes):
        image = self.get_image_by_id(image_id)
        image.resized_binary_data = resized_binary_data
        self.db.commit()

    def get_image_by_id(self, image_id: int):
        return self.db.query(Image).filter_by(id=image_id).first()

    def get_latest_images(self, limit: int = 10):
        return self.db.query(Image).order_by(Image.time_created.desc()).limit(limit).all()
