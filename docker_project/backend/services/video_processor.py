"""
Video processing service
"""

import subprocess
import logging
from pathlib import Path
from typing import Tuple

from ..config import settings

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handles video processing through COLMAP pipeline"""

    def __init__(self):
        self.script_path = settings.SCRIPTS_DIR / settings.PIPELINE_SCRIPT

    def check_script_exists(self) -> bool:
        """Check if the pipeline script exists and is executable"""
        return self.script_path.exists() and self.script_path.is_file()

    async def process(self, video_path: Path, fps: int) -> Tuple[bool, str]:
        """
        Process video through COLMAP pipeline

        Args:
            video_path: Path to the video file
            fps: Frames per second for extraction

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.check_script_exists():
            return False, f"Pipeline script not found: {self.script_path}"

        try:
            logger.info(f"Starting pipeline: {self.script_path}")
            logger.info(f"Video: {video_path}, FPS: {fps}")

            # Build command
            cmd = [str(self.script_path), str(video_path), "colmap_project", str(fps)]

            logger.info(f"Executing: {' '.join(cmd)}")

            # Execute pipeline
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.PIPELINE_TIMEOUT,
                cwd="/app/LichtFeld-Studio",
            )

            # Log output
            if result.stdout:
                logger.info(f"Pipeline stdout:\n{result.stdout}")
            if result.stderr:
                logger.warning(f"Pipeline stderr:\n{result.stderr}")

            # Check result
            if result.returncode != 0:
                error_msg = f"Pipeline failed with code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr}"
                return False, error_msg

            # Verify output
            if not settings.COLMAP_PROJECT_DIR.exists():
                return False, "COLMAP project directory was not created"

            # Check if directory is not empty
            if not any(settings.COLMAP_PROJECT_DIR.iterdir()):
                return False, "COLMAP project directory is empty"

            return True, "Processing completed successfully"

        except subprocess.TimeoutExpired:
            logger.error("Pipeline execution timeout")
            return False, f"Processing timeout exceeded ({settings.PIPELINE_TIMEOUT}s)"
        except Exception as e:
            logger.error(f"Pipeline execution error: {str(e)}", exc_info=True)
            return False, f"Pipeline execution error: {str(e)}"
