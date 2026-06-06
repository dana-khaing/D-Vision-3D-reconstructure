"""
Phase 0 — Step 3: SAM2 Person Masking Test
Tests SAM2 + YOLOv8 person masking on a folder of images.
Usage: python pipeline/03_sam2_test.py --images /path/to/photos --output /tmp/masks
"""

import argparse
import os
import time
import gc
from pathlib import Path

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")


def run(image_dir: Path, output_dir: Path) -> None:
    import torch
    import numpy as np
    from PIL import Image

    output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    print(f"\nDevice:  {device}")
    print(f"Images:  {image_dir}")
    print(f"Output:  {output_dir}\n")

    image_paths = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.JPG"))
    if not image_paths:
        print("No .jpg files found in image directory.")
        return
    print(f"Found {len(image_paths)} images\n")

    # Load YOLO
    print("Loading YOLOv8n...")
    from ultralytics import YOLO
    yolo = YOLO("yolov8n.pt")

    # Load SAM2
    print("Loading SAM2 ViT-B+...")
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    sam2_ckpt = Path.home() / "models/sam2/sam2.1_hiera_base_plus.pt"
    if not sam2_ckpt.exists():
        print(f"✗ SAM2 checkpoint not found: {sam2_ckpt}")
        print("  Download: https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_base_plus.pt")
        return

    sam2 = build_sam2("configs/sam2.1/sam2.1_hiera_b+.yaml", str(sam2_ckpt), device=device)
    predictor = SAM2ImagePredictor(sam2)

    total_people = 0
    t_total = time.time()

    for i, img_path in enumerate(image_paths):
        t = time.time()
        img_np = np.array(Image.open(img_path).convert("RGB"))
        H, W = img_np.shape[:2]
        final_mask = np.zeros((H, W), dtype=bool)

        results = yolo(img_np, classes=[0], verbose=False)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        n_people = len(boxes)
        total_people += n_people

        if n_people > 0:
            with torch.inference_mode():
                predictor.set_image(img_np)
                for box in boxes:
                    masks, _, _ = predictor.predict(box=box, multimask_output=False)
                    final_mask |= masks[0].astype(bool)

        # Save mask
        out = output_dir / (img_path.stem + "_mask.png")
        Image.fromarray((final_mask.astype(np.uint8) * 255)).save(out)

        elapsed = time.time() - t
        mask_pct = final_mask.mean() * 100
        print(f"  [{i+1:3}/{len(image_paths)}] {img_path.name}: "
              f"{n_people} people, {mask_pct:.1f}% masked, {elapsed:.1f}s")

        if (i + 1) % 10 == 0:
            if hasattr(torch.mps, "empty_cache"):
                torch.mps.empty_cache()
            gc.collect()

    total_elapsed = time.time() - t_total
    throughput = len(image_paths) / total_elapsed * 60

    print(f"\n── Results ──────────────────────────────────────────────────")
    print(f"  Images processed: {len(image_paths)}")
    print(f"  Total people:     {total_people}")
    print(f"  Total time:       {total_elapsed/60:.1f} min")
    print(f"  Throughput:       {throughput:.1f} images/min")
    print(f"  Masks saved to:   {output_dir}")

    if throughput >= 5:
        print("  ✓ MPS acceleration working")
    else:
        print("  ⚠ Slow throughput — check MPS fallback ops")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--output", default=Path("/tmp/sam2_masks"), type=Path)
    args = parser.parse_args()
    run(args.images, args.output)
