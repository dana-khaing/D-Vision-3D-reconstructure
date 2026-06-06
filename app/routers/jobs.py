import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database import get_session
from app.models.job import ProcessingJob
from app.models.event import Event

router = APIRouter(tags=["jobs"])


class ProcessRequest(BaseModel):
    quality: str = "standard"  # draft | standard | high
    window_ids: Optional[List[str]] = None


class JobRead(BaseModel):
    id: str
    event_id: str
    status: str
    stage: Optional[str]
    progress_pct: int
    quality: str
    error_msg: Optional[str]
    retry_count: int
    enqueued_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_sec: Optional[int]


@router.post("/events/{event_id}/process", response_model=JobRead, status_code=202)
async def trigger_processing(
    event_id: str,
    req: ProcessRequest,
    session: AsyncSession = Depends(get_session),
):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    job = ProcessingJob(
        event_id=event_id,
        quality=req.quality,
        window_ids=json.dumps(req.window_ids) if req.window_ids else None,
    )
    session.add(job)
    event.status = "processing"
    session.add(event)
    await session.commit()
    await session.refresh(job)

    # TODO: enqueue to ARQ — will be wired in worker/settings.py
    # await arq_pool.enqueue_job("run_pipeline", job.id, event_id)

    return job


@router.get("/jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(ProcessingJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs/{job_id}/cancel", response_model=JobRead)
async def cancel_job(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(ProcessingJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = "cancelled"
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


@router.post("/jobs/{job_id}/retry", response_model=JobRead)
async def retry_job(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(ProcessingJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.retry_count >= job.max_retries:
        raise HTTPException(status_code=400, detail="Max retries reached")
    job.status = "queued"
    job.retry_count += 1
    job.error_msg = None
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job
