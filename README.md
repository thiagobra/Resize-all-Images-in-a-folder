# Resize all Images in a Folder

A small Python utility that batch-resizes every JPEG and PNG image in a directory.

## Install

```bash
pip install -r requirements.txt
```

Requires Python 3.9+ and Pillow 9.1+. `tqdm` is used for the progress bar.

## Usage

```bash
python "python code to rezise it.py" /path/to/folder
```

By default, every `.jpg` / `.jpeg` / `.png` file (case-insensitive) in the given
folder is resized into a 1024×600 box, **preserving aspect ratio**, and saved
next to the original with a `resized_` prefix.

### Common examples

```bash
# Recurse into subdirectories
python "python code to rezise it.py" -r /path/to/folder

# Crop to fill instead of fitting inside the box
python "python code to rezise it.py" --mode fit /path/to/folder

# Convert everything to WebP at quality 80
python "python code to rezise it.py" --format webp --quality 80 /path/to/folder

# See what would happen without writing anything
python "python code to rezise it.py" --dry-run /path/to/folder

# Resize 4 images at a time
python "python code to rezise it.py" --workers 4 /path/to/folder
```

### All flags

| Flag                 | Description                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| `directory`          | Folder to process (positional).                                             |
| `--mode`             | `contain` (default), `fit`, or `stretch`.                                   |
| `--format`           | Output extension: `jpeg`, `jpg`, `png`, `webp`, `bmp`, `tiff`.              |
| `-r`, `--recursive`  | Walk subdirectories.                                                        |
| `--dry-run`          | List targets without writing.                                               |
| `--quality N`        | JPEG/WebP quality (1–100).                                                  |
| `--optimize`         | Encoder-side optimization (smaller files, slower save).                     |
| `--max-pixels N`     | Override Pillow's decompression-bomb limit (`0` disables).                  |
| `--workers N`        | Parallel worker threads (default 1).                                        |
| `-q`, `--quiet`      | Only warnings/errors.                                                       |
| `-v`, `--verbose`    | Include debug-level logs.                                                   |

The script is also importable for tests:

```python
from importlib import import_module  # see tests/ for the loader pattern
```

## Output

Files are written next to their source as `resized_<original>` (or
`resized_<basename>.<format>` if `--format` is set). Files already starting with
`resized_` are skipped, so re-running is idempotent.

## Behavior notes

- Mixed-case extensions (`.JPG`, `.PNG`) are matched.
- EXIF orientation is honored — phone photos won't come out sideways.
- Per-file errors (corrupt files, decompression bombs) are logged as warnings
  and the batch continues.

## License

[MIT](LICENSE) © Thiago Augusto Braga.

## Security

See [SECURITY.md](SECURITY.md) for how to privately report vulnerabilities.
