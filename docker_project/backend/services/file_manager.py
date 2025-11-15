"""
File management service
"""

import shutil
import tempfile
import logging
from pathlib import Path
from fastapi import UploadFile

from config import settings

logger = logging.getLogger(__name__)


class FileManager:
    """Handles file operations for video processing"""

    async def save_upload(self, video: UploadFile) -> Path:
        """
        Save uploaded video to data directory

        Args:
            video: Uploaded video file

        Returns:
            Path to saved video file
        """
        video_path = settings.DATA_DIR / settings.VIDEO_FILENAME

        try:
            # Save video file
            with open(video_path, "wb") as buffer:
                # Read and write in chunks to handle large files
                while chunk := await video.read(8192):
                    buffer.write(chunk)

            logger.info(
                f"Video saved: {video_path} ({video_path.stat().st_size} bytes)"
            )
            return video_path

        except Exception as e:
            logger.error(f"Failed to save video: {str(e)}", exc_info=True)
            # Clean up partial file if it exists
            if video_path.exists():
                video_path.unlink()
            raise

    def cleanup_colmap_project(self):
        """Remove existing COLMAP project directory"""
        if settings.COLMAP_PROJECT_DIR.exists():
            try:
                shutil.rmtree(settings.COLMAP_PROJECT_DIR)
                logger.info(
                    f"Cleaned up old COLMAP project: {settings.COLMAP_PROJECT_DIR}"
                )
                # Recreate empty directory
                settings.COLMAP_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to cleanup COLMAP project: {str(e)}")
                raise

    def create_zip(self) -> Path:
        """
        Create ZIP archive of COLMAP project

        Returns:
            Path to created ZIP file
        """
        if not settings.COLMAP_PROJECT_DIR.exists():
            raise FileNotFoundError("COLMAP project directory not found")

        try:
            # Create temporary file for ZIP
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            zip_path = Path(temp_file.name)
            temp_file.close()

            # Create ZIP archive
            logger.info(f"Creating ZIP archive: {zip_path}")
            shutil.make_archive(
                str(zip_path.with_suffix("")), "zip", settings.COLMAP_PROJECT_DIR
            )

            logger.info(f"ZIP created: {zip_path} ({zip_path.stat().st_size} bytes)")
            return zip_path

        except Exception as e:
            logger.error(f"Failed to create ZIP: {str(e)}", exc_info=True)
            raise

    def cleanup_temp_files(self):
        """Clean up temporary files (called periodically)"""
        # This could be expanded to clean up old temporary files
        pass
