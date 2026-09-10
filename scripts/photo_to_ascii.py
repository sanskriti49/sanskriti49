"""Convert Sanskriti's profile photo to an accurate, attractive, and non-distorted terminal ASCII portrait."""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from scipy.ndimage import label, binary_dilation


# Monospace dimensions fitting 460x420 terminal screen
COLS = 76
ROWS = 40

# Face-friendly ASCII ramp (smooth light skin, distinct eyes/smile/hair)
CHARS = "   ..::--==++**##%%@@"
GAMMA = 1.6


def convert_photo_to_ascii(source_path: Path, destination_path: Path) -> None:
    im = Image.open(source_path).convert("RGB")
    
    # 1. Optimal crop centered on Sanskriti (excludes distracting curtain on left)
    # Original image is 1600 x 1202.
    crop_box = (400, 40, 1500, 1140)
    cropped = im.crop(crop_box)
    
    # 2. Mask the background wall so the portrait silhouette is clean
    arr = np.array(cropped, dtype=float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    brightness = (r + g + b) / 3.0
    saturation = np.max(arr, axis=2) - np.min(arr, axis=2)
    
    # Background wall is low-saturation, bright, and slightly bluish-gray
    wall_candidate = (brightness > 95) & (saturation < 30) & (b >= r - 15)
    
    labeled, _ = label(wall_candidate)
    top_border_labels = np.unique(np.concatenate([
        labeled[0, :],
        labeled[:300, -1],
        labeled[:200, 0]
    ]))
    top_border_labels = top_border_labels[top_border_labels > 0]
    external_wall_mask = np.isin(labeled, top_border_labels)
    external_wall_mask = binary_dilation(external_wall_mask, iterations=2)
    
    gray = np.array(cropped.convert("L"), dtype=float)
    # Set external background to pure white (renders as clean space in ASCII)
    gray[external_wall_mask] = 255.0
    cleaned = Image.fromarray(np.uint8(gray))
    
    # 3. Enhance facial features (smile, eyes, eyeliner, wavy hair waves)
    sharp = cleaned.filter(ImageFilter.UnsharpMask(radius=1.8, percent=220, threshold=2))
    enhanced = ImageEnhance.Contrast(sharp).enhance(1.45)
    fit = ImageOps.fit(enhanced, (COLS, ROWS), method=Image.Resampling.LANCZOS)
    arr_fit = np.array(fit, dtype=float)
    
    # 4. Generate ASCII lines
    rows = []
    for r_idx in range(ROWS):
        line = []
        for c_idx in range(COLS):
            val = arr_fit[r_idx, c_idx]
            if val >= 248:
                line.append(" ")
            else:
                norm = (val / 248.0) ** GAMMA
                idx = int((1.0 - norm) * (len(CHARS) - 1))
                idx = max(0, min(len(CHARS) - 1, idx))
                line.append(CHARS[idx])
        rows.append("".join(line))
        
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text("\n".join(rows), encoding="utf-8")
    print(f"Generated ASCII art: cols={COLS} rows={ROWS} -> {destination_path}")


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/profile-photo.jpg")
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("assets/profile-ascii.txt")
    convert_photo_to_ascii(source, destination)


if __name__ == "__main__":
    main()
