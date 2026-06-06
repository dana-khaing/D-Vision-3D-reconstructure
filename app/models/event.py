import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    status: str = Field(default="created")  # created|processing|done|failed
    settings: Optional[str] = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
