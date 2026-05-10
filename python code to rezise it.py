"""Resize all JPEG and PNG images in a directory to 1024x600."""

# pip install Pillow

from __future__ import annotations

import argparse
import os

from PIL import Image, ImageOps


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resize all JPEG and PNG images in a directory to 1024x600.",
    )
    parser.add_argument(
        "directory",
        help="Path to the folder containing images to resize.",
    )
    return parser.parse_args(argv)


def resize_directory(directory: str) -> None:
    for file in os.listdir(directory):
        if file.endswith(("jpeg", "png", "jpg")):
            outfile = os.path.join(directory, "resized_" + file)
            with Image.open(os.path.join(directory, file)) as im:
                # im.resize((1024, 600), resample=None, box=(50,50,200,200), reducing_gap=None) **DIDN'T WORK**
                new_size = im.resize((1024, 600), resample=None, box=None, reducing_gap=None)
                # im = ImageOps.pad(im, (1024, 600), color='grey')**DIDN'T WORK**
                # im = ImageOps.fit(im, (1024, 600))**DIDN'T WORK**
                new_size.save(outfile)
                # im.save(outfile)
    print("finished! check the folder to see if it worked!")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    resize_directory(args.directory)


if __name__ == "__main__":
    main()
