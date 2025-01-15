import os
import locale
import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
import SocialScores.Database.InitializationJob as InitializationJob
from SocialScores.Services.ResizeService import ResizeService
from SocialScores.Controllers.PostController import router as post_router
from SocialScores.Controllers.ImageController import router as image_router
from SocialScores.Controllers.AccountController import router as account_router

print(f"Preferred encoding: {locale.getpreferredencoding()}")

resize_service = ResizeService()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        print("Starting application...")
        InitializationJob.start()
        resize_service.start()
        print("Database initialization complete.")
        yield
    except Exception as e:
        print(f"Error during application startup: {e}")
        raise
    finally:
        print("Shutting down ResizeService...")
        resize_service.stop()
        print("Application is shutting down...")

app = FastAPI(
    title="Social Scores API",
    version="1.0.0",
    description="API for managing social scores with PostgreSQL.",
    lifespan=app_lifespan,
)

try:
    with open("openapi.json", "r") as file:
        openapi_schema = json.load(file)
    app.openapi_schema = openapi_schema
    print("OpenAPI schema loaded successfully.")
except FileNotFoundError:
    print("Error: openapi.json not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding openapi.json: {e}")

app.include_router(account_router, prefix="/api/v1/account", tags=["Account"])
app.include_router(post_router, prefix="/api/v1/post", tags=["Post"])
app.include_router(image_router, prefix="/api/v1/image", tags=["Image"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Scores API"}
