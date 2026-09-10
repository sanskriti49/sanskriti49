"""Convert the profile photo to a compact terminal portrait."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps


CHARS = " .:-=+*#%@"
CHAR_ASPECT_RATIO = 0.55
COLS = 82
FONT_SIZE = 8.0
LINE_HEIGHT = 8.5


def main() -> None:
    source, destination = map(Path, sys.argv[1:3])
    image = Image.open(source).convert("L")
    image = image.crop((300, 40, 1500, 1120))
    rows = round((image.height / image.width) * COLS * CHAR_ASPECT_RATIO)
    image = ImageOps.fit(image, (COLS, rows), method=Image.Resampling.LANCZOS, centering=(0.56, 0.42))
    image = ImageOps.autocontrast(image, cutoff=2)
    pixels = [255 - pixel for pixel in image.getdata()]
    rows = []
    for offset in range(0, len(pixels), image.width):
        rows.append("".join(CHARS[pixel * (len(CHARS) - 1) // 255] for pixel in pixels[offset : offset + image.width]))
    destination.write_text("\n".join(rows), encoding="utf-8")
    print(
        f"ASCII geometry: cols={image.width} rows={image.height} "
        f"charAspectRatio={CHAR_ASPECT_RATIO:.2f} fontSize={FONT_SIZE:.1f}px lineHeight={LINE_HEIGHT:.1f}px "
        "targetPanel=460x420",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
