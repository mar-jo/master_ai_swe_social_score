from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
from pathlib import Path

UPLOAD_FOLDER = "uploads"

# Ensure the upload directory exists
upload_path = Path(UPLOAD_FOLDER)
if not upload_path.exists():
    upload_path.mkdir(parents=True, exist_ok=True)

# Create a router for the ImageController
router = APIRouter()

@router.post("/")
async def post_image(file: UploadFile):
    """
    Save an uploaded image to the server.
    """
    try:
        # Define the upload path
        file_path = upload_path / file.filename

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": f"File {file.filename} uploaded successfully.", "file_path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload the file: {str(e)}")

@router.get("/{file_name}")
async def get_image(file_name: str):
    """
    Retrieve an image by file name.
    """
    try:
        # Define the file path
        file_path = upload_path / file_name

        # Check if the file exists
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found.")

        # Return the file as a response
        return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve the file: {str(e)}")
