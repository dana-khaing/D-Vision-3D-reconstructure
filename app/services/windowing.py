"""Auto-generate time windows from photo EXIF timestamps."""

from datetime import datetime, timedelta
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.photo import Photo
from app.models.window import TimeWindow


async def auto_create_windows(
    event_id: str,
    session: AsyncSession,
    window_minutes: int = 15,
    overlap_minutes: int = 5,
    min_photos: int = 20,
) -> List[TimeWindow]:
    result = await session.exec(
        select(Photo)
        .where(Photo.event_id == event_id, Photo.taken_at.is_not(None))
        .order_by(Photo.taken_at)
    )
    photos = result.all()

    if not photos:
        return []

    event_start = photos[0].taken_at
    event_end = photos[-1].taken_at
    step = timedelta(minutes=window_minutes - overlap_minutes)
    window = timedelta(minutes=window_minutes)

    windows: List[TimeWindow] = []
    current = event_start
    sort_order = 0

    while current < event_end:
        end = current + window
        bucket = [p for p in photos if p.taken_at and current <= p.taken_at <= end]

        if len(bucket) >= min_photos:
            tw = TimeWindow(
                event_id=event_id,
                start_ts=current,
                end_ts=end,
                photo_count=len(bucket),
                sort_order=sort_order,
                label=current.strftime("%I:%M %p"),
            )
            session.add(tw)
            windows.append(tw)
            sort_order += 1

        current += step

    await session.commit()
    return windows
