from fastapi import FastAPI
from starlette.responses import FileResponse
from SocialScores.Controllers import account_controller, post_controller
from SocialScores.Database.DatabaseFactory import DatabaseFactory

app = FastAPI()

# Include API routes
app.include_router(account_controller.router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(post_controller.router, prefix="/api/v1/posts", tags=["Posts"])

# Serve OpenAPI definition if needed
@app.get("/openapi.json")
def get_openapi_definition():
    return FileResponse("SocialScores/openapi.json")
