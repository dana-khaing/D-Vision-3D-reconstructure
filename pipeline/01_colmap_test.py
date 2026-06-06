"""
Phase 0 — Step 1: COLMAP Test
Tests COLMAP on a folder of your own photos.
Usage: python pipeline/01_colmap_test.py --images /path/to/your/photos
"""

import argparse
import time
from pathlib import Path

import pycolmap


def run(image_dir: Path, workspace: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    db = workspace / "database.db"
    sparse = workspace / "sparse"
    sparse.mkdir(exist_ok=True)

    print(f"\nImages:    {image_dir}")
    print(f"Workspace: {workspace}")
    n_images = len(list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.JPG")))
    print(f"Photos:    {n_images}\n")

    # ── Step 1: Feature Extraction ──────────────────────────────────────────
    print("Step 1/3: Feature extraction...")
    t = time.time()
    opts = pycolmap.SiftExtractionOptions()
    opts.max_num_features = 16384
    opts.estimate_affine_shape = True
    opts.domain_size_pooling = True   # key for dark photos

    pycolmap.extract_features(
        database_path=str(db),
        image_path=str(image_dir),
        sift_options=opts,
        camera_mode=pycolmap.CameraMode.PER_IMAGE,
        verbose=False,
    )
    print(f"  Done in {time.time()-t:.1f}s")

    # ── Step 2: Feature Matching ────────────────────────────────────────────
    print("Step 2/3: Feature matching (exhaustive)...")
    t = time.time()
    match_opts = pycolmap.SiftMatchingOptions()
    match_opts.guided_matching = True
    pycolmap.match_exhaustive(database_path=str(db), sift_options=match_opts, verbose=False)
    print(f"  Done in {time.time()-t:.1f}s")

    # ── Step 3: Sparse Reconstruction ───────────────────────────────────────
    print("Step 3/3: Incremental mapping...")
    t = time.time()
    mapper_opts = pycolmap.IncrementalPipelineOptions()
    mapper_opts.ba_refine_focal_length = True
    maps = pycolmap.incremental_mapping(
        database_path=str(db),
        image_path=str(image_dir),
        output_path=str(sparse),
        options=mapper_opts,
    )
    elapsed = time.time() - t
    print(f"  Done in {elapsed:.1f}s\n")

    # ── Results ─────────────────────────────────────────────────────────────
    if not maps:
        print("✗ COLMAP produced no reconstruction.")
        print("  → Add more photos or use a better-lit scene.")
        return

    best = max(maps.values(), key=lambda r: r.num_reg_images())
    reg = best.num_reg_images()
    pts = best.num_points3D()
    errors = [p.error for p in best.points3D.values()]
    mean_err = sum(errors) / len(errors) if errors else 0

    print("── Results ─────────────────────────────────────────────────")
    print(f"  Reconstructions:   {len(maps)}")
    print(f"  Registered images: {reg} / {n_images} ({reg/max(n_images,1):.0%})")
    print(f"  3D points:         {pts:,}")
    print(f"  Mean repro. error: {mean_err:.2f} px")
    print()

    if reg / max(n_images, 1) >= 0.7 and pts >= 5000 and mean_err <= 2.0:
        print("✓ COLMAP quality: GOOD — safe to proceed to OpenSplat")
    elif reg / max(n_images, 1) >= 0.5:
        print("⚠ COLMAP quality: ACCEPTABLE — results may have gaps")
    else:
        print("✗ COLMAP quality: POOR — add more overlapping photos")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, type=Path, help="Directory of JPEG photos")
    parser.add_argument("--workspace", default=Path("/tmp/colmap_test"), type=Path)
    args = parser.parse_args()
    run(args.images, args.workspace)
