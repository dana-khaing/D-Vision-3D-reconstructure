import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class ProcessingJob(SQLModel, table=True):
    __tablename__ = "processing_jobs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    event_id: str = Field(foreign_key="events.id", index=True)
    window_ids: Optional[str] = None     # JSON list of window IDs
    status: str = Field(default="queued", index=True)  # queued|running|done|failed|cancelled
    stage: Optional[str] = None          # colmap|sam2|depth|splat|done
    progress_pct: int = 0
    quality: str = Field(default="standard")  # draft|standard|high
    error_msg: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_sec: Optional[int] = None
