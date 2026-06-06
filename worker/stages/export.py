"""Export stage — post-process .ply and assemble scene.json for the viewer."""

import json
from datetime import datetime
from pathlib import Path
from app.services.storage import event_output_dir


async def run_export(ctx: dict, job_id: str, event_id: str, workspace: Path) -> None:
    ply_src = workspace / "outputs" / "scene.ply"
    out_dir = event_output_dir(event_id)

    # Copy .ply to public outputs directory
    import shutil
    dest_ply = out_dir / "foundation.ply"
    shutil.copy2(ply_src, dest_ply)

    # Count Gaussians from PLY header
    gaussian_count = _count_ply_vertices(dest_ply)
    ply_size_mb = dest_ply.stat().st_size / 1e6

    # Parse PSNR from training log
    psnr = _parse_final_psnr(workspace / "opensplat.log")

    scene_meta = {
        "event_id": event_id,
        "generated_at": datetime.utcnow().isoformat(),
        "foundation_ply": "foundation.ply",
        "gaussian_count": gaussian_count,
        "ply_size_mb": round(ply_size_mb, 2),
        "psnr": psnr,
        "windows": [],
    }

    scene_json = out_dir / "scene.json"
    scene_json.write_text(json.dumps(scene_meta, indent=2))


def _count_ply_vertices(ply_path: Path) -> int:
    try:
        with open(ply_path, "rb") as f:
            for line in f:
                text = line.decode("ascii", errors="ignore").strip()
                if text.startswith("element vertex"):
                    return int(text.split()[-1])
                if text == "end_header":
                    break
    except Exception:
        pass
    return -1


def _parse_final_psnr(log_path: Path) -> float | None:
    if not log_path.exists():
        return None
    last_psnr = None
    try:
        for line in log_path.read_text(errors="ignore").splitlines():
            if "PSNR" in line:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == "PSNR:" and i + 1 < len(parts):
                        try:
                            last_psnr = float(parts[i + 1])
                        except ValueError:
                            pass
    except Exception:
        pass
    return last_psnr
