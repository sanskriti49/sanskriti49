"""Convert the profile photo to a compact terminal portrait."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps


CHARS = " .,:;irsXA253hMHGS#9B&@"


def main() -> None:
    source, destination = map(Path, sys.argv[1:3])
    image = Image.open(source).convert("L")
    image = ImageOps.fit(image, (62, 34), method=Image.Resampling.LANCZOS, centering=(0.56, 0.42))
    image = ImageOps.autocontrast(image, cutoff=2)
    pixels = list(image.getdata())
    rows = []
    for offset in range(0, len(pixels), image.width):
        rows.append("".join(CHARS[pixel * (len(CHARS) - 1) // 255] for pixel in pixels[offset : offset + image.width]))
    destination.write_text("\n".join(rows), encoding="utf-8")


if __name__ == "__main__":
    main()
