"""File storage helpers — local filesystem, cloud-ready interface."""

from pathlib import Path
from app.config import settings


def event_upload_dir(event_id: str) -> Path:
    d = settings.uploads_dir / event_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def event_workspace_dir(event_id: str) -> Path:
    d = settings.workspaces_dir / event_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def event_output_dir(event_id: str) -> Path:
    d = settings.outputs_dir / event_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def checkpoint_path(event_id: str, stage: str) -> Path:
    return event_workspace_dir(event_id) / "checkpoints" / f"{stage}_done"


def write_checkpoint(event_id: str, stage: str) -> None:
    p = checkpoint_path(event_id, stage)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()


def checkpoint_exists(event_id: str, stage: str) -> bool:
    return checkpoint_path(event_id, stage).exists()
