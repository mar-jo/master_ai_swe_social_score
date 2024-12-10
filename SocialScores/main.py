import os
import locale
import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
import SocialScores.Database.InitializationJob as InitializationJob
from SocialScores.Controllers.PostController import router as post_router
from SocialScores.Controllers.ImageController import router as image_router
from SocialScores.Controllers.AccountController import router as account_router

# Print encoding for debugging
print(f"Preferred encoding: {locale.getpreferredencoding()}")

# Define lifespan for application startup and shutdown
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        print("Starting application...")
        InitializationJob.start()  # Ensure database tables and test data are initialized
        print("Database initialization complete.")
        yield
    except Exception as e:
        print(f"Error during application startup: {e}")
        raise
    finally:
        print("Application is shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Social Scores API",
    version="1.0.0",
    description="API for managing social scores with PostgreSQL.",
    lifespan=app_lifespan,
)

# Load OpenAPI schema and validate
try:
    with open("openapi.json", "r") as file:
        openapi_schema = json.load(file)
    app.openapi_schema = openapi_schema
    print("OpenAPI schema loaded successfully.")
except FileNotFoundError:
    print("Error: openapi.json not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding openapi.json: {e}")

# Include routers for endpoints
app.include_router(account_router, prefix="/api/v1/account", tags=["Account"])
app.include_router(post_router, prefix="/api/v1/post", tags=["Post"])
app.include_router(image_router, prefix="/api/v1/image", tags=["Image"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Social Scores API"}
