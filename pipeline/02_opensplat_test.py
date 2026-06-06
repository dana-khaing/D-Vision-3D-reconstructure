"""
Phase 0 — Step 2: OpenSplat Test
Trains a Gaussian Splat from an existing COLMAP workspace.
Usage: python pipeline/02_opensplat_test.py --workspace /tmp/colmap_test --iters 5000
"""

import argparse
import subprocess
import time
import os
from pathlib import Path


def find_opensplat() -> Path:
    candidates = [
        Path.home() / "OpenSplat/build/opensplat",
        Path("/usr/local/bin/opensplat"),
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        "OpenSplat binary not found.\n"
        "Build from source: https://github.com/pierotofy/OpenSplat\n"
        "  git clone --recursive https://github.com/pierotofy/OpenSplat\n"
        "  cd OpenSplat && mkdir build && cd build\n"
        "  cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(sysctl -n hw.logicalcpu)"
    )


def run(workspace: Path, output: Path, iters: int) -> None:
    opensplat = find_opensplat()
    output.mkdir(parents=True, exist_ok=True)
    ply_out = output / "test_scene.ply"

    print(f"\nOpenSplat: {opensplat}")
    print(f"Workspace: {workspace}")
    print(f"Output:    {ply_out}")
    print(f"Iters:     {iters}\n")

    cmd = [
        str(opensplat),
        str(workspace),
        "--output-point-cloud", str(ply_out),
        "--iterations", str(iters),
        "--num-downscales", "2",
        "--sh-degree", "1" if iters < 10000 else "3",
        "--max-cap-gaussians", "500000" if iters < 10000 else "1000000",
    ]

    env = {**os.environ, "PYTORCH_ENABLE_MPS_FALLBACK": "1"}
    t_start = time.time()

    print("Training (this will take a while)...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             env=env, text=True)

    last_psnr = None
    iter_count = 0

    for line in proc.stdout:
        if "PSNR" in line or "Loss" in line:
            print(f"  {line.strip()}")
            if "PSNR" in line:
                try:
                    parts = line.split()
                    idx = parts.index("PSNR:")
                    last_psnr = float(parts[idx + 1])
                except (ValueError, IndexError):
                    pass

    proc.wait()
    elapsed = time.time() - t_start

    print(f"\n── Results ──────────────────────────────────────────────────")
    print(f"  Exit code:  {proc.returncode}")
    print(f"  Time:       {elapsed/60:.1f} min")
    if last_psnr:
        print(f"  Final PSNR: {last_psnr:.2f} dB")
        if last_psnr >= 25:
            print("  ✓ Quality: GOOD")
        elif last_psnr >= 20:
            print("  ⚠ Quality: ACCEPTABLE")
        else:
            print("  ✗ Quality: POOR — check COLMAP reconstruction first")

    if ply_out.exists():
        size_mb = ply_out.stat().st_size / 1e6
        print(f"  PLY size:   {size_mb:.1f} MB")
        print(f"\n✓ Open in Supersplat: https://playcanvas.com/supersplat")
        print(f"  Drag and drop: {ply_out}\n")
    else:
        print("  ✗ No PLY file produced. Check error output above.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=Path("/tmp/colmap_test"), type=Path,
                        help="COLMAP workspace from 01_colmap_test.py")
    parser.add_argument("--output", default=Path("/tmp/opensplat_test"), type=Path)
    parser.add_argument("--iters", default=5000, type=int,
                        help="Iterations (5000=fast preview, 30000=full quality)")
    args = parser.parse_args()
    run(args.workspace, args.output, args.iters)
