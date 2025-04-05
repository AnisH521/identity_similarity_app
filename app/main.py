from fastapi import FastAPI
import uvicorn

from app.api.routes import router as api_router

app = FastAPI(
    title="Identity Verification API",
    description="API for comparing face images and text data for identity verification",
    version="1.0.0"
)

# Include routers
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Identity Verification API is running. Go to /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)