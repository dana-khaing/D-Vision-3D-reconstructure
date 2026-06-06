import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database import get_session
from app.models.event import Event

router = APIRouter(prefix="/events", tags=["events"])


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None


class EventRead(BaseModel):
    id: str
    name: str
    description: Optional[str]
    event_date: Optional[datetime]
    status: str
    created_at: datetime


@router.post("", response_model=EventRead, status_code=201)
async def create_event(data: EventCreate, session: AsyncSession = Depends(get_session)):
    event = Event(**data.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@router.get("", response_model=List[EventRead])
async def list_events(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Event).order_by(Event.created_at.desc()))
    return result.all()


@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: str, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: str, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await session.delete(event)
    await session.commit()
