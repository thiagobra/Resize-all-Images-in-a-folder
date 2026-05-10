"""Resize all JPEG and PNG images in a directory to 1024x600."""

# pip install Pillow

from __future__ import annotations

import argparse
import os

from PIL import Image, ImageOps


DEFAULT_SIZE = (1024, 600)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resize all JPEG and PNG images in a directory to 1024x600.",
    )
    parser.add_argument(
        "directory",
        help="Path to the folder containing images to resize.",
    )
    parser.add_argument(
        "--mode",
        choices=("contain", "fit", "stretch"),
        default="contain",
        help=(
            "How to fit the image into the target size. "
            "'contain' preserves aspect ratio and fits inside the target (default). "
            "'fit' preserves aspect ratio and crops to fill the target. "
            "'stretch' ignores aspect ratio (legacy behavior)."
        ),
    )
    return parser.parse_args(argv)


def _resize_image(im: Image.Image, mode: str, size: tuple[int, int]) -> Image.Image:
    if mode == "stretch":
        return im.resize(size)
    if mode == "contain":
        return ImageOps.contain(im, size)
    if mode == "fit":
        return ImageOps.fit(im, size)
    raise ValueError(f"unknown mode: {mode!r}")


def resize_directory(
    directory: str,
    mode: str = "contain",
    size: tuple[int, int] = DEFAULT_SIZE,
) -> None:
    for file in os.listdir(directory):
        if file.startswith("resized_"):
            continue
        if file.lower().endswith(("jpeg", "png", "jpg")):
            outfile = os.path.join(directory, "resized_" + file)
            with Image.open(os.path.join(directory, file)) as im:
                out = _resize_image(im, mode, size)
                out.save(outfile)
    print("finished! check the folder to see if it worked!")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    resize_directory(args.directory, mode=args.mode)


if __name__ == "__main__":
    main()
