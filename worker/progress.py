"""Publish pipeline progress events to Redis PubSub → WebSocket clients."""

import json
from datetime import datetime


async def report(ctx: dict, job_id: str, stage: str, pct: int, msg: str = "") -> None:
    redis = ctx.get("redis")
    if not redis:
        return
    payload = json.dumps({
        "job_id": job_id,
        "stage": stage,
        "pct": pct,
        "msg": msg,
        "ts": datetime.utcnow().isoformat(),
    })
    await redis.publish(f"job:{job_id}:progress", payload)
