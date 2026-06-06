"""
Phase 0 — Step 0: Environment Check
Run this first to verify every tool is installed and MPS is working.
Usage: python pipeline/00_env_check.py
"""

import sys
import subprocess
from pathlib import Path

PASS = "✓"
FAIL = "✗"
WARN = "⚠"


def check(label: str, fn) -> bool:
    try:
        result = fn()
        print(f"  {PASS}  {label}: {result}")
        return True
    except Exception as e:
        print(f"  {FAIL}  {label}: {e}")
        return False


def main():
    print("\n── Python ─────────────────────────────────────────────────")
    check("Python version", lambda: f"{sys.version}")

    print("\n── PyTorch / MPS ──────────────────────────────────────────")
    def torch_check():
        import torch
        mps = torch.backends.mps.is_available()
        return f"torch {torch.__version__} | MPS={'available' if mps else 'NOT available'}"
    check("torch + MPS", torch_check)

    def mps_compute():
        import torch
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS not available")
        x = torch.ones(512, 512, device="mps")
        result = (x @ x).sum().item()
        return f"MPS matrix multiply OK (result={result:.0f})"
    check("MPS compute test", mps_compute)

    print("\n── pycolmap ────────────────────────────────────────────────")
    def colmap_check():
        import pycolmap
        return f"pycolmap {pycolmap.__version__}"
    check("pycolmap import", colmap_check)

    print("\n── COLMAP binary ───────────────────────────────────────────")
    def colmap_bin():
        r = subprocess.run(["colmap", "help"], capture_output=True, text=True)
        return "colmap binary found"
    check("colmap CLI", colmap_bin)

    print("\n── SAM2 ────────────────────────────────────────────────────")
    def sam2_check():
        from sam2.build_sam import build_sam2
        return "SAM2 importable"
    check("sam2 import", sam2_check)

    print("\n── ultralytics (YOLOv8) ────────────────────────────────────")
    def yolo_check():
        from ultralytics import YOLO
        return "ultralytics importable"
    check("ultralytics import", yolo_check)

    print("\n── OpenSplat binary ────────────────────────────────────────")
    def opensplat_check():
        from pathlib import Path
        candidates = [
            Path.home() / "OpenSplat/build/opensplat",
            Path("/usr/local/bin/opensplat"),
        ]
        for c in candidates:
            if c.exists():
                return f"found at {c}"
        raise FileNotFoundError(
            "Not found. Build from: https://github.com/pierotofy/OpenSplat"
        )
    check("opensplat binary", opensplat_check)

    print("\n── Image libraries ─────────────────────────────────────────")
    check("Pillow", lambda: __import__("PIL").__version__ if hasattr(__import__("PIL"), "__version__") else "ok")
    check("piexif", lambda: (__import__("piexif"), "ok")[1])
    check("opencv-python", lambda: __import__("cv2").__version__)
    check("open3d", lambda: __import__("open3d").__version__)
    check("imagehash", lambda: (__import__("imagehash"), "ok")[1])

    print("\n── Done. Fix any ✗ items before running the pipeline. ──────\n")


if __name__ == "__main__":
    main()
