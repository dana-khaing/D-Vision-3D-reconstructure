import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TimeWindow(SQLModel, table=True):
    __tablename__ = "time_windows"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    event_id: str = Field(foreign_key="events.id", index=True)
    label: Optional[str] = None          # "Cocktail Hour", "Dinner", etc.
    start_ts: datetime
    end_ts: datetime
    photo_count: int = 0
    sort_order: int = 0
    ply_path: Optional[str] = None
    ply_size_mb: Optional[float] = None
    splat_count: Optional[int] = None
    psnr: Optional[float] = None         # reconstruction quality metric
    status: str = Field(default="pending")  # pending|processing|done|failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
