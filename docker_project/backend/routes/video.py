"""
Video processing routes
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import logging

from services.video_processor import VideoProcessor
from services.file_manager import FileManager
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/api", tags=["video"])

video_processor = VideoProcessor()
file_manager = FileManager()


@router.post("/process")
async def process_video(
    video: UploadFile = File(..., description="Video file to process"),
    fps: int = Form(
        ...,
        description="Frames per second for extraction",
        ge=settings.MIN_FPS,
        le=settings.MAX_FPS,
    ),
):
    """
    Process uploaded video through COLMAP pipeline

    Args:
        video: Video file upload
        fps: Frames per second for frame extraction

    Returns:
        ZIP file containing the COLMAP project
    """
    try:
        logger.info(f"Received video: {video.filename}, FPS: {fps}")

        # Validate video file
        if not video.content_type or not video.content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be a video")

        # Save uploaded video
        video_path = await file_manager.save_upload(video)
        logger.info(f"Video saved to: {video_path}")

        # Clean up old COLMAP project
        file_manager.cleanup_colmap_project()

        # Process video through pipeline
        success, message = await video_processor.process(video_path, fps)

        if not success:
            raise HTTPException(status_code=500, detail=message)

        logger.info("Processing completed successfully")

        # Create and return ZIP file
        zip_path = file_manager.create_zip()

        return FileResponse(
            path=str(zip_path),
            media_type="application/zip",
            filename="colmap_project.zip",
            background=None,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/status")
async def get_status():
    """Check if pipeline script is available"""
    script_available = video_processor.check_script_exists()
    return {
        "pipeline_available": script_available,
        "data_dir": str(settings.DATA_DIR),
        "colmap_project_dir": str(settings.COLMAP_PROJECT_DIR),
    }
