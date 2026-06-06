import uuid
import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database import get_session
from app.models.photo import Photo
from app.models.event import Event
from app.config import settings
from app.services.upload import extract_exif, compute_blur_score

router = APIRouter(prefix="/events/{event_id}/photos", tags=["photos"])


class PhotoRead(BaseModel):
    id: str
    event_id: str
    filename: str
    file_size: int | None
    taken_at: datetime | None
    camera_make: str | None
    camera_model: str | None
    blur_score: float | None
    created_at: datetime


@router.post("", response_model=List[PhotoRead], status_code=201)
async def upload_photos(
    event_id: str,
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    upload_dir = settings.uploads_dir / event_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    created: List[Photo] = []
    for file in files:
        photo_id = str(uuid.uuid4())
        dest = upload_dir / f"{photo_id}_{file.filename}"

        with dest.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        exif = extract_exif(dest)
        blur = compute_blur_score(dest)

        photo = Photo(
            id=photo_id,
            event_id=event_id,
            filename=file.filename or dest.name,
            file_path=str(dest),
            file_size=dest.stat().st_size,
            blur_score=blur,
            **exif,
        )
        session.add(photo)
        created.append(photo)

    await session.commit()
    for p in created:
        await session.refresh(p)
    return created


@router.get("", response_model=List[PhotoRead])
async def list_photos(event_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(Photo).where(Photo.event_id == event_id).order_by(Photo.taken_at)
    )
    return result.all()


@router.delete("/{photo_id}", status_code=204)
async def delete_photo(
    event_id: str, photo_id: str, session: AsyncSession = Depends(get_session)
):
    photo = await session.get(Photo, photo_id)
    if not photo or photo.event_id != event_id:
        raise HTTPException(status_code=404, detail="Photo not found")
    Path(photo.file_path).unlink(missing_ok=True)
    await session.delete(photo)
    await session.commit()
