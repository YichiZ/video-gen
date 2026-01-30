"""Video generation endpoints."""

import asyncio
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse
from google import genai

from backend.models.schemas import (
    OperationItem,
    OperationsListResponse,
    VideoGenerationRequest,
    VideoGenerationResponse,
    VideoGenerationStatusResponse,
)

router = APIRouter()

# In-memory storage for operations (use Redis/database in production)
operations_store: dict[str, dict] = {}

# Directory to store generated videos (relative to backend directory)
VIDEOS_DIR = Path(__file__).parent.parent / "generated_videos"
VIDEOS_DIR.mkdir(exist_ok=True)


def get_client() -> genai.Client:
    """Get Google GenAI client."""
    # Client will use GOOGLE_API_KEY environment variable
    return genai.Client()


@router.post("/video/generate", response_model=VideoGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
) -> VideoGenerationResponse:
    """
    Generate a video using Veo3.

    This endpoint starts an asynchronous video generation process.
    Use the returned operation_id to check status via /video/status/{operation_id}
    """
    try:
        client = get_client()

        # Start video generation
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=request.prompt,
        )

        print(operation)
        # Extract operation ID (operation.name format: models/veo-3.1-generate-preview/operations/b1pmfb9s860x)
        if hasattr(operation, 'name') and operation.name:
            # Extract just the last part after the final '/'
            operation_id = operation.name.split('/')[-1]
        else:
            operation_id = str(id(operation))

        # Store operation info (store the operation object reference)
        operations_store[operation_id] = {
            "operation": operation,
            "status": "pending",
            "prompt": request.prompt,
            "video_path": None,
            "error": None,
        }

        # Poll in background
        background_tasks.add_task(poll_video_generation, operation_id)

        return VideoGenerationResponse(
            operation_id=operation_id,
            status="pending",
            message="Video generation started. Use the operation_id to check status.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start video generation: {str(e)}",
        )


async def poll_video_generation(operation_id: str):
    """Background task to poll video generation status and download when ready."""
    if operation_id not in operations_store:
        return

    client = get_client()
    operation = operations_store[operation_id]["operation"]

    try:
        # Poll until operation is done
        while not operation.done:
            operations_store[operation_id]["status"] = "processing"
            await asyncio.sleep(10)
            # Refresh operation status
            operation = client.operations.get(operation)
            operations_store[operation_id]["operation"] = operation

        # Download the generated video
        if hasattr(operation, 'response') and hasattr(operation.response, 'generated_videos'):
            generated_video = operation.response.generated_videos[0]

            # Save video to file
            video_filename = f"{operation_id}.mp4"
            video_path = VIDEOS_DIR / video_filename

            client.files.download(file=generated_video.video)
            generated_video.video.save(str(video_path))

            operations_store[operation_id]["status"] = "completed"
            operations_store[operation_id]["video_path"] = str(video_path)
        else:
            operations_store[operation_id]["status"] = "failed"
            operations_store[operation_id]["error"] = "No video generated in response"

    except Exception as e:
        operations_store[operation_id]["status"] = "failed"
        operations_store[operation_id]["error"] = str(e)


@router.get("/video/status/{operation_id}", response_model=VideoGenerationStatusResponse)
async def get_video_status(operation_id: str) -> VideoGenerationStatusResponse:
    """Get the status of a video generation operation."""
    if operation_id not in operations_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operation {operation_id} not found",
        )

    operation_data = operations_store[operation_id]
    status_value = operation_data["status"]

    video_url = None
    if status_value == "completed" and operation_data.get("video_path"):
        video_url = f"/api/v1/video/download/{operation_id}"

    # Use error message if it exists and is not None, otherwise use status message
    error = operation_data.get("error")
    message = error if error else f"Status: {status_value}"

    return VideoGenerationStatusResponse(
        operation_id=operation_id,
        status=status_value,
        video_url=video_url,
        message=message,
    )


@router.get("/video/download/{operation_id}")
async def download_video(operation_id: str) -> FileResponse:
    """Download a generated video."""
    if operation_id not in operations_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operation {operation_id} not found",
        )

    operation_data = operations_store[operation_id]

    if operation_data["status"] != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video generation not completed. Current status: {operation_data['status']}",
        )

    video_path = operation_data.get("video_path")
    if not video_path or not Path(video_path).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video file not found",
        )

    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=f"{operation_id}.mp4",
    )


@router.get("/video/operations", response_model=OperationsListResponse)
async def get_all_operations() -> OperationsListResponse:
    """Get all video generation operations."""
    operations_list = []
    
    for operation_id, operation_data in operations_store.items():
        video_url = None
        if operation_data["status"] == "completed" and operation_data.get("video_path"):
            video_url = f"/api/v1/video/download/{operation_id}"
        
        operations_list.append(
            OperationItem(
                operation_id=operation_id,
                status=operation_data["status"],
                prompt=operation_data.get("prompt", ""),
                video_path=operation_data.get("video_path"),
                error=operation_data.get("error"),
                video_url=video_url,
            )
        )
    
    return OperationsListResponse(
        operations=operations_list,
        total=len(operations_list),
    )
