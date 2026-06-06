"""OpenSplat stage — train 3D Gaussian Splatting model per time window."""

import asyncio
import subprocess
import os
from pathlib import Path
from app.config import settings


async def run_opensplat(ctx: dict, job_id: str, event_id: str, workspace: Path) -> None:
    colmap_dir = workspace / "colmap"
    mask_dir = workspace / "masks"
    output_dir = workspace / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    ply_out = output_dir / "scene.ply"

    if not settings.opensplat_bin.exists():
        raise FileNotFoundError(
            f"OpenSplat binary not found at {settings.opensplat_bin}. "
            "Build from source: https://github.com/pierotofy/OpenSplat"
        )

    cmd = [
        str(settings.opensplat_bin),
        str(colmap_dir),
        "--output-point-cloud", str(ply_out),
        "--iterations", str(settings.opensplat_iterations),
        "--num-downscales", "2",
        "--sh-degree", "3",
        "--max-cap-gaussians", str(settings.max_gaussians),
        "--densify-from-iter", "500",
        "--densify-until-iter", "15000",
        "--opacity-reset-interval", "3000",
        "--keep-crs",
    ]

    if mask_dir.exists() and any(mask_dir.glob("*.png")):
        cmd += ["--masks", str(mask_dir)]

    env = {**os.environ, "PYTORCH_ENABLE_MPS_FALLBACK": "1"}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=env,
    )

    log_path = workspace / "opensplat.log"
    with open(log_path, "w") as log_f:
        async for line in proc.stdout:
            decoded = line.decode(errors="ignore")
            log_f.write(decoded)
            log_f.flush()

            # Monitor memory via log parsing
            if "PSNR" in decoded:
                pass  # could extract psnr here for progress updates

    await proc.wait()

    if proc.returncode != 0:
        raise RuntimeError(
            f"OpenSplat failed (exit {proc.returncode}). "
            f"Check {log_path} for details."
        )

    if not ply_out.exists():
        raise RuntimeError("OpenSplat finished but no .ply file was produced.")
