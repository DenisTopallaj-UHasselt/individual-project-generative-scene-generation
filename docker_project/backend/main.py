"""
FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from routes import video
from config import settings

app = FastAPI(
    title="LichtFeld Video Processor API",
    description="Upload videos and process them through COLMAP pipeline",
    version="1.0.0",
)

# Include routers
app.include_router(video.router)

# Mount static files
STATIC_DIR = Path(__file__).parent.parent / "frontend" / "static"
TEMPLATES_DIR = Path(__file__).parent.parent / "frontend" / "templates"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main HTML page"""
    index_path = TEMPLATES_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text())
    return HTMLResponse(content="<h1>Frontend not found</h1>")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "data_dir": str(settings.DATA_DIR),
        "colmap_project_dir": str(settings.COLMAP_PROJECT_DIR),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
