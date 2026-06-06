"""COLMAP stage — Structure from Motion to estimate camera poses."""

import asyncio
from pathlib import Path


async def run_colmap(ctx: dict, job_id: str, event_id: str, workspace: Path) -> None:
    import pycolmap

    image_dir = workspace / "images"
    database_path = workspace / "colmap" / "database.db"
    sparse_dir = workspace / "colmap" / "sparse"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    sparse_dir.mkdir(parents=True, exist_ok=True)

    # Feature extraction — tuned for dark/party photos
    extract_opts = pycolmap.SiftExtractionOptions()
    extract_opts.max_num_features = 16384
    extract_opts.estimate_affine_shape = True
    extract_opts.domain_size_pooling = True

    pycolmap.extract_features(
        database_path=str(database_path),
        image_path=str(image_dir),
        sift_options=extract_opts,
        camera_mode=pycolmap.CameraMode.PER_IMAGE,
        verbose=False,
    )

    # Exhaustive matching (switch to vocab tree for > 200 photos)
    match_opts = pycolmap.SiftMatchingOptions()
    match_opts.max_ratio = 0.88
    match_opts.guided_matching = True

    pycolmap.match_exhaustive(
        database_path=str(database_path),
        sift_options=match_opts,
        verbose=False,
    )

    # Incremental mapping
    mapper_opts = pycolmap.IncrementalPipelineOptions()
    mapper_opts.min_num_matches = 15
    mapper_opts.ba_refine_focal_length = True
    mapper_opts.ba_refine_extra_params = True

    maps = pycolmap.incremental_mapping(
        database_path=str(database_path),
        image_path=str(image_dir),
        output_path=str(sparse_dir),
        options=mapper_opts,
    )

    if not maps:
        raise RuntimeError(
            "COLMAP produced no reconstruction. "
            "Check photo overlap and lighting quality."
        )

    best = max(maps.values(), key=lambda r: r.num_reg_images())
    reg_rate = best.num_reg_images() / max(len(list(image_dir.glob("*.jpg"))), 1)

    if reg_rate < 0.5:
        raise RuntimeError(
            f"Only {reg_rate:.0%} of photos registered. "
            "Add more photos from different angles."
        )
