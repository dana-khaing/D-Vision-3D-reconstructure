import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.config import settings

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/jobs/{job_id}")
async def job_progress_ws(websocket: WebSocket, job_id: str):
    """Stream live pipeline progress via Redis PubSub."""
    await websocket.accept()
    try:
        import redis.asyncio as aioredis

        r = aioredis.from_url(settings.redis_url, decode_responses=True)
        async with r.pubsub() as ps:
            await ps.subscribe(f"job:{job_id}:progress")
            async for message in ps.listen():
                if message["type"] == "message":
                    await websocket.send_text(message["data"])
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
