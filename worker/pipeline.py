"""Main pipeline orchestrator — chains COLMAP → SAM2 → OpenSplat per time window."""

import asyncio
from pathlib import Path

from app.services.storage import checkpoint_exists, write_checkpoint, event_workspace_dir
from worker.progress import report
from worker.stages.colmap import run_colmap
from worker.stages.sam2 import run_sam2
from worker.stages.opensplat import run_opensplat
from worker.stages.export import run_export


STAGES = [
    ("ingest",   None,          10,  "Preparing photos"),
    ("colmap",   run_colmap,    40,  "Mapping photo positions in 3D space"),
    ("sam2",     run_sam2,      60,  "Masking people from scene"),
    ("splat",    run_opensplat, 90,  "Building your 3D scene"),
    ("export",   run_export,    100, "Finalising"),
]


async def run_pipeline(ctx: dict, job_id: str, event_id: str) -> dict:
    """ARQ task — runs the full ML pipeline for one event."""
    workspace = event_workspace_dir(event_id)

    try:
        for stage_name, stage_fn, target_pct, label in STAGES:
            if checkpoint_exists(event_id, stage_name):
                await report(ctx, job_id, stage_name, target_pct, f"{label} (cached)")
                continue

            await report(ctx, job_id, stage_name, target_pct - 15, label)

            if stage_fn is not None:
                await stage_fn(ctx, job_id, event_id, workspace)

            write_checkpoint(event_id, stage_name)
            await report(ctx, job_id, stage_name, target_pct, f"{label} done")

        return {"status": "done", "job_id": job_id, "event_id": event_id}

    except asyncio.CancelledError:
        await report(ctx, job_id, "cancelled", 0, "Job was cancelled")
        raise

    except Exception as exc:
        await report(ctx, job_id, "error", 0, str(exc))
        raise
