"""Resize all JPEG and PNG images in a directory to 1024x600."""

# pip install Pillow

from __future__ import annotations

import argparse
import logging
import os

from PIL import Image, ImageOps, UnidentifiedImageError


log = logging.getLogger(__name__)

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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be processed without writing any output.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=None,
        metavar="N",
        help="JPEG/WebP quality (1-100). Default: Pillow's per-format default.",
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Pass optimize=True to the encoder (smaller files, slower save).",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Only show warnings and errors.",
    )
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show debug-level logs.",
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


def _select_targets(directory: str, recursive: bool) -> list[tuple[str, str]]:
    return [
        (root, name)
        for root, name in _iter_image_files(directory, recursive)
        if not name.startswith("resized_") and name.lower().endswith(("jpeg", "png", "jpg"))
    ]


def _progress(iterable, total: int):
    try:
        from tqdm import tqdm
    except ImportError:
        return iterable
    return tqdm(iterable, total=total, unit="img")


def resize_directory(
    directory: str,
    mode: str = "contain",
    size: tuple[int, int] = DEFAULT_SIZE,
    recursive: bool = False,
    format: str | None = None,
    dry_run: bool = False,
    quality: int | None = None,
    optimize: bool = False,
) -> None:
    save_kwargs: dict[str, object] = {}
    if quality is not None:
        save_kwargs["quality"] = quality
    if optimize:
        save_kwargs["optimize"] = True

    targets = _select_targets(directory, recursive)
    log.info("processing %d image(s)%s", len(targets), " (dry run)" if dry_run else "")
    for root, file in _progress(targets, len(targets)):
        infile = os.path.join(root, file)
        outfile = _output_path(root, file, format)
        if dry_run:
            log.info("would write %s", outfile)
            continue
        try:
            with Image.open(infile) as im:
                im = ImageOps.exif_transpose(im)
                out = _resize_image(im, mode, size)
                out.save(outfile, **save_kwargs)
            log.debug("wrote %s", outfile)
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            log.warning("skipping %s: %s", infile, exc)
    log.info("finished! check the folder to see if it worked!")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    level = logging.WARNING if args.quiet else logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    logging.getLogger("PIL").setLevel(logging.INFO)
    if args.max_pixels is not None:
        Image.MAX_IMAGE_PIXELS = args.max_pixels or None
    resize_directory(
        args.directory,
        mode=args.mode,
        recursive=args.recursive,
        format=args.format,
        dry_run=args.dry_run,
        quality=args.quality,
        optimize=args.optimize,
    )


if __name__ == "__main__":
    main()
