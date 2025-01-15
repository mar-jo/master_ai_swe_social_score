from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io
import imghdr
from sqlalchemy.orm import Session
from SocialScores.Database.RepositoryAccount import RepositoryAccount
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Controllers.PostController import PostController
from SocialScores.Controllers.ImageController import ImageController
from SocialScores.Models.Account import AccountRegister, AccountLogin, AccountResponse
from SocialScores.Database.Database import get_db

class AccountController:
    def __init__(self, db: Session):
        self.repo = RepositoryAccount(db)

    def register(self, account: AccountRegister):
        try:
            new_account = self.repo.create_account(
                email=account.email,
                username=account.username,
                password=account.password
            )
            return {"message": "Account registered successfully", "id": new_account.id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def login(self, account: AccountLogin):
        try:
            account = self.repo.validate_login(account.username, account.password)
            return {"message": "Login successful", "id": account.id}
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    def get_account_by_id(self, account_id: int):
        account = self.repo.get_account_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def get_accounts_random(self, count: int):
        return self.repo.get_accounts_random(count)

    def get_posts_for_account(self, account_id: int):
        posts = self.repo.get_posts_for_account(account_id)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this account")
        return posts

    def get_highscores(self, limit: int = 10):
        return self.repo.get_highscores(limit)

    def update_socialscore(self, account_id: int, delta: int):
        try:
            return self.repo.update_socialscore(account_id, delta)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

router = APIRouter()

@router.post("/register")
def register(account: AccountRegister, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.register(account)

@router.post("/login")
def login(account: AccountLogin, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.login(account)

@router.get("/explore")
def get_accounts_random(count: int = 10, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.get_accounts_random(count)

@router.get("/posts")
def get_posts_by_account(account_id: int, db: Session = Depends(get_db)):
    controller = PostController(db)
    return controller.get_posts_for_account(account_id)

@router.get("/info")
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.get_account_by_id(account_id)

@router.get("/highscores")
def get_highscores(limit: int = 10, db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.get_highscores(limit)

@router.post("/update-socialscore")
def update_socialscore(account_id: int = Form(...), delta: int = Form(...), db: Session = Depends(get_db)):
    controller = AccountController(db)
    return controller.update_socialscore(account_id, delta)

@router.post("/profile-picture")
def upload_profile_picture(account_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    account_repo = RepositoryAccount(db)
    image_repo = RepositoryImage(db)

    binary_data = image.file.read()
    new_image = image_repo.add_image(
        filename=image.filename,
        binary_data=binary_data,
        uploader=str(account_id)
    )

    ImageController.send_resize_request(new_image.id)

    updated_account = account_repo.update_profile_image(account_id, new_image.id)
    return {"message": "Profile picture updated", "account": updated_account}

@router.get("/get-profile-picture")
def get_profile_picture(account_id: int, size: str = "full", db: Session = Depends(get_db)):
    account_repo = RepositoryAccount(db)

    account = account_repo.get_account_by_id(account_id)
    if not account or not account.profile_image:
        raise HTTPException(status_code=404, detail="Profile picture not found")

    image = account.profile_image

    if size == "resized" and image.resized_binary_data:
        binary_data = image.resized_binary_data
    elif size == "full" and image.binary_data:
        binary_data = image.binary_data
    else:
        raise HTTPException(status_code=400, detail="Requested image size not available")

    import imghdr
    image_type = imghdr.what(None, binary_data)
    mime_type = f"image/{image_type}" if image_type else "application/octet-stream"

    return StreamingResponse(io.BytesIO(binary_data), media_type=mime_type)