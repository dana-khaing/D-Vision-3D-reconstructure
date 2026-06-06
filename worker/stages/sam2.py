"""SAM2 stage — segment people out of each photo before Gaussian Splatting."""

import os
import gc
from pathlib import Path


async def run_sam2(ctx: dict, job_id: str, event_id: str, workspace: Path) -> None:
    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

    import torch
    from app.config import settings

    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

    image_dir = workspace / "images"
    mask_dir = workspace / "masks"
    mask_dir.mkdir(parents=True, exist_ok=True)

    image_paths = sorted(image_dir.glob("*.jpg")) + sorted(image_dir.glob("*.JPG"))

    # Load YOLO for person detection
    from ultralytics import YOLO
    yolo = YOLO("yolov8n.pt")

    # Load SAM2
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    sam2 = build_sam2(
        "configs/sam2.1/sam2.1_hiera_b+.yaml",
        str(settings.sam2_checkpoint),
        device=device,
    )
    predictor = SAM2ImagePredictor(sam2)

    import numpy as np
    from PIL import Image

    for img_path in image_paths:
        out_path = mask_dir / (img_path.stem + "_mask.png")
        if out_path.exists():
            continue

        img_np = np.array(Image.open(img_path).convert("RGB"))
        H, W = img_np.shape[:2]
        final_mask = np.zeros((H, W), dtype=bool)

        results = yolo(img_np, classes=[0], verbose=False)  # class 0 = person
        boxes = results[0].boxes.xyxy.cpu().numpy()

        if len(boxes) > 0:
            with torch.inference_mode():
                predictor.set_image(img_np)
                for box in boxes:
                    masks, _, _ = predictor.predict(box=box, multimask_output=False)
                    final_mask |= masks[0].astype(bool)

            # Dilate mask 20px to catch motion-blur halos
            import cv2
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
            final_mask = cv2.dilate(final_mask.astype(np.uint8), kernel) > 0

        mask_img = Image.fromarray((final_mask.astype(np.uint8) * 255))
        mask_img.save(out_path)

        # Release MPS memory every 10 images
        if len(list(mask_dir.glob("*.png"))) % 10 == 0:
            torch.mps.empty_cache() if hasattr(torch.mps, "empty_cache") else None
            gc.collect()
