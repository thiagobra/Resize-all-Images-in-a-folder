"""Resize all JPEG and PNG images in a directory to 1024x600."""

# pip install Pillow

from __future__ import annotations

import argparse
import os

from PIL import Image, ImageOps, UnidentifiedImageError


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
    parser.add_argument(
        "--max-pixels",
        type=int,
        default=None,
        help=(
            "Override Pillow's MAX_IMAGE_PIXELS decompression-bomb threshold. "
            "Pass a larger value to allow legitimate huge images, or 0 to disable the check."
        ),
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories. Outputs are written next to each source file.",
    )
    parser.add_argument(
        "--format",
        choices=("jpeg", "jpg", "png", "webp", "bmp", "tiff"),
        default=None,
        help="Output format extension. Defaults to preserving the source extension.",
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


def _iter_image_files(directory: str, recursive: bool):
    if recursive:
        for root, _dirs, files in os.walk(directory):
            for name in files:
                yield root, name
    else:
        for name in os.listdir(directory):
            yield directory, name


def _output_path(root: str, file: str, format: str | None) -> str:
    if format is None:
        return os.path.join(root, "resized_" + file)
    base = os.path.splitext(file)[0]
    return os.path.join(root, f"resized_{base}.{format}")


def resize_directory(
    directory: str,
    mode: str = "contain",
    size: tuple[int, int] = DEFAULT_SIZE,
    recursive: bool = False,
    format: str | None = None,
) -> None:
    for root, file in _iter_image_files(directory, recursive):
        if file.startswith("resized_"):
            continue
        if not file.lower().endswith(("jpeg", "png", "jpg")):
            continue
        infile = os.path.join(root, file)
        outfile = _output_path(root, file, format)
        try:
            with Image.open(infile) as im:
                im = ImageOps.exif_transpose(im)
                out = _resize_image(im, mode, size)
                out.save(outfile)
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            print(f"skipping {infile}: {exc}")
    print("finished! check the folder to see if it worked!")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.max_pixels is not None:
        Image.MAX_IMAGE_PIXELS = args.max_pixels or None
    resize_directory(
        args.directory,
        mode=args.mode,
        recursive=args.recursive,
        format=args.format,
    )


if __name__ == "__main__":
    main()
