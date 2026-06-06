"""EXIF extraction and image quality utilities for uploaded photos."""

from pathlib import Path
from typing import Any, Dict
from datetime import datetime


def extract_exif(path: Path) -> Dict[str, Any]:
    """Return a dict of EXIF fields for a photo file."""
    result: Dict[str, Any] = {
        "taken_at": None,
        "gps_lat": None,
        "gps_lon": None,
        "camera_make": None,
        "camera_model": None,
        "focal_length": None,
        "iso": None,
        "width": None,
        "height": None,
    }
    try:
        import piexif
        from PIL import Image

        img = Image.open(path)
        result["width"], result["height"] = img.size

        exif_bytes = img.info.get("exif")
        if not exif_bytes:
            return result

        exif = piexif.load(exif_bytes)
        ifd0 = exif.get("0th", {})
        exif_ifd = exif.get("Exif", {})
        gps_ifd = exif.get("GPS", {})

        make = ifd0.get(piexif.ImageIFD.Make)
        model = ifd0.get(piexif.ImageIFD.Model)
        result["camera_make"] = make.decode(errors="ignore").strip("\x00") if make else None
        result["camera_model"] = model.decode(errors="ignore").strip("\x00") if model else None

        dt_str = exif_ifd.get(piexif.ExifIFD.DateTimeOriginal)
        if dt_str:
            try:
                result["taken_at"] = datetime.strptime(
                    dt_str.decode(errors="ignore"), "%Y:%m:%d %H:%M:%S"
                )
            except ValueError:
                pass

        fl = exif_ifd.get(piexif.ExifIFD.FocalLength)
        if fl and fl[1]:
            result["focal_length"] = fl[0] / fl[1]

        iso = exif_ifd.get(piexif.ExifIFD.ISOSpeedRatings)
        if iso:
            result["iso"] = iso

        if gps_ifd:
            lat = _dms_to_decimal(gps_ifd.get(piexif.GPSIFD.GPSLatitude))
            lon = _dms_to_decimal(gps_ifd.get(piexif.GPSIFD.GPSLongitude))
            lat_ref = gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef, b"N")
            lon_ref = gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef, b"E")
            if lat and lon:
                result["gps_lat"] = lat if lat_ref == b"N" else -lat
                result["gps_lon"] = lon if lon_ref == b"E" else -lon

    except Exception:
        pass

    return result


def _dms_to_decimal(dms) -> float | None:
    if not dms or len(dms) < 3:
        return None
    try:
        d = dms[0][0] / dms[0][1]
        m = dms[1][0] / dms[1][1]
        s = dms[2][0] / dms[2][1]
        return d + m / 60 + s / 3600
    except (ZeroDivisionError, TypeError):
        return None


def compute_blur_score(path: Path) -> float | None:
    """Laplacian variance — lower = blurrier. Returns None if cv2 unavailable."""
    try:
        import cv2
        import numpy as np

        img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        return float(cv2.Laplacian(img, cv2.CV_64F).var())
    except Exception:
        return None
