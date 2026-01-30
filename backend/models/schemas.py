"""Pydantic schemas for request/response models."""

from pydantic import BaseModel, Field


class VideoGenerationRequest(BaseModel):
    """Request model for video generation."""
    
    prompt: str = Field(
        ...,
        description="Text prompt describing the video to generate",
        min_length=1,
        max_length=5000,
    )


class VideoGenerationResponse(BaseModel):
    """Response model for video generation."""
    
    operation_id: str = Field(..., description="Operation ID for tracking the video generation")
    status: str = Field(..., description="Current status of the operation")
    message: str = Field(..., description="Status message")


class VideoGenerationStatusResponse(BaseModel):
    """Response model for video generation status."""
    
    operation_id: str = Field(..., description="Operation ID")
    status: str = Field(..., description="Current status (pending, processing, completed, failed)")
    video_url: str | None = Field(None, description="URL to download the generated video if completed")
    message: str = Field(..., description="Status message")


class OperationItem(BaseModel):
    """Model for a single operation in the operations list."""
    
    operation_id: str = Field(..., description="Operation ID")
    status: str = Field(..., description="Current status (pending, processing, completed, failed)")
    prompt: str = Field(..., description="Prompt used for video generation")
    video_path: str | None = Field(None, description="Path to generated video file if completed")
    error: str | None = Field(None, description="Error message if generation failed")
    video_url: str | None = Field(None, description="URL to download the generated video if completed")


class OperationsListResponse(BaseModel):
    """Response model for listing all operations."""
    
    operations: list[OperationItem] = Field(..., description="List of all operations")
    total: int = Field(..., description="Total number of operations")
