import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Photo(SQLModel, table=True):
    __tablename__ = "photos"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    event_id: str = Field(foreign_key="events.id", index=True)
    filename: str
    file_path: str
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None

    # EXIF fields
    taken_at: Optional[datetime] = Field(default=None, index=True)
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    focal_length: Optional[float] = None
    iso: Optional[int] = None
    blur_score: Optional[float] = None  # Laplacian variance

    # Processing state
    colmap_image_id: Optional[int] = None
    is_registered: bool = False
    window_id: Optional[str] = Field(default=None, foreign_key="time_windows.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
