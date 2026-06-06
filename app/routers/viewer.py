import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database import get_session
from app.models.event import Event
from app.models.window import TimeWindow
from app.config import settings

router = APIRouter(tags=["viewer"])


@router.get("/events/{event_id}/scene")
async def get_scene_metadata(event_id: str, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    result = await session.exec(
        select(TimeWindow)
        .where(TimeWindow.event_id == event_id)
        .order_by(TimeWindow.sort_order)
    )
    windows = result.all()

    return {
        "event_id": event_id,
        "event_name": event.name,
        "status": event.status,
        "windows": [
            {
                "id": w.id,
                "label": w.label,
                "start_ts": w.start_ts.isoformat() if w.start_ts else None,
                "end_ts": w.end_ts.isoformat() if w.end_ts else None,
                "photo_count": w.photo_count,
                "ply_url": f"/ply/{event_id}/{w.id}.ply" if w.ply_path else None,
                "status": w.status,
                "psnr": w.psnr,
            }
            for w in windows
        ],
    }


@router.get("/ply/{event_id}/{window_id}.ply")
async def serve_ply(event_id: str, window_id: str):
    ply_path = settings.outputs_dir / event_id / f"{window_id}.ply"
    if not ply_path.exists():
        raise HTTPException(status_code=404, detail="PLY file not found")
    return FileResponse(
        path=str(ply_path),
        media_type="application/octet-stream",
        filename=f"{window_id}.ply",
        headers={"Accept-Ranges": "bytes"},
    )


@router.get("/thumbnails/{photo_id}.webp")
async def serve_thumbnail(photo_id: str):
    thumb = settings.uploads_dir / "thumbnails" / f"{photo_id}.webp"
    if not thumb.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(path=str(thumb), media_type="image/webp")
