# CLAUDE.md

## Project Overview

This is a minimal Python utility that batch-resizes all JPEG and PNG images in a specified directory. It was created by Thiago Augusto Braga in November 2022.

## Repository Structure

```
Resize-all-Images-in-a-folder/
├── README.md
└── python code to rezise it.py   # Main script (note: filename has a typo — "rezise")
```

There are no tests, no package configuration, and no CI/CD pipelines.

## The Script

**File**: `python code to rezise it.py`

**What it does**:
1. Iterates over every file in a target directory.
2. Filters for files ending in `jpeg`, `png`, or `jpg`.
3. Resizes each image to **1024×600** pixels using Pillow's `Image.resize()`.
4. Saves the result with a `resized_` prefix in the same directory.

**Key detail**: the target directory is hardcoded on line 9:
```python
directory = 'C:\\Users\\Thiago\\Desktop'  # SPECIFY THE DIRECTORY!
```
Any user running this script must change that path to their own directory.

**Dependency**: [Pillow](https://pillow.readthedocs.io/) (`pip install Pillow`).

## Development Conventions

- **Single-file, script-style code** — there is no package structure, no `main()` guard, and no CLI argument handling.
- **No requirements file** — the only dependency is Pillow, documented only as a comment inside the script.
- **Commented-out alternatives** — the script retains `# ...DIDN'T WORK` comments from earlier experiments with `ImageOps.pad` and `ImageOps.fit`. Preserve these as historical context unless explicitly removing them.
- **No aspect-ratio preservation** — despite the README saying "Keeping it aspect ratio", the current implementation uses a fixed `(1024, 600)` target and does NOT preserve the original aspect ratio. This is a known discrepancy.

## How to Run

```bash
pip install Pillow
# Edit the `directory` variable in the script to point to your image folder
python "python code to rezise it.py"
```

Output images appear in the same folder with the `resized_` prefix.

## Common Tasks for AI Assistants

### Adding CLI argument support
The most impactful improvement is replacing the hardcoded `directory` variable with `argparse` so users can pass the path at runtime:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()
directory = args.directory
```

### Preserving aspect ratio
To match the README's stated goal, replace the fixed resize with a thumbnail/contain approach:
```python
im.thumbnail((1024, 600))      # shrinks in-place, preserves ratio
# or
ImageOps.contain(im, (1024, 600))  # Pillow ≥ 9.1
```

### Adding a requirements.txt
```
Pillow>=9.0
```

### Supported image formats
The current filter (`jpeg`, `png`, `jpg`) does **not** include uppercase extensions (`.JPEG`, `.PNG`, `.JPG`) or other Pillow-supported formats (`.bmp`, `.gif`, `.tiff`, `.webp`). Use `file.lower().endswith(...)` to handle mixed-case filenames.

## Git Branches

- `main` — stable history; original code lives here.
- `claude/add-claude-documentation-LMSCm` — branch used for adding this documentation.

## Notes

- The script filename contains a spelling error ("rezise" instead of "resize"). Do **not** rename the file unless explicitly asked, as it matches the original repository naming.
- There are no tests. When making changes, manually run the script against a folder of sample images to verify output.
