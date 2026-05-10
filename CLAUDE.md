# CLAUDE.md

## Project Overview

A small Python utility that batch-resizes JPEG and PNG images in a directory. Created by Thiago Augusto Braga in November 2022; significantly expanded since (CLI, tests, CI, packaging).

## Repository Structure

```
Resize-all-Images-in-a-folder/
├── resize_images.py             # Main script (importable module + CLI entry)
├── pyproject.toml               # Project metadata, ruff/mypy/pytest/coverage config, hatch build
├── requirements.txt             # Runtime deps (Pillow, tqdm)
├── README.md                    # User-facing docs
├── CONTRIBUTING.md              # Dev workflow
├── CHANGELOG.md                 # Keep a Changelog format
├── SECURITY.md                  # Private vulnerability reporting policy
├── LICENSE                      # MIT
├── .pre-commit-config.yaml      # ruff + mypy + standard hooks
├── .github/
│   ├── workflows/ci.yml         # Matrix: {ubuntu, macos, windows} × {3.10..3.13}
│   ├── dependabot.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/{bug_report,feature_request,config}.yml
└── tests/
    ├── conftest.py              # Loads resize_images.py via importlib (legacy filename support)
    └── test_resize.py           # 16 tests, ~96% coverage
```

**Filename history**: The script was originally named `python code to rezise it.py` (with a misspelling and embedded spaces). It was renamed to `resize_images.py` in branch `claude/review-clause-md-9u8fk` to make the module importable and pip-installable. CHANGELOG.md and the corresponding issue (#12) document the change.

## The Script

**File**: `resize_images.py` (importable module).

**Entry points**:
- Module: `python resize_images.py /path/to/folder [flags]`
- Console script (after `pip install .`): `resize-images /path/to/folder [flags]`
- Programmatic: `from resize_images import main, resize_directory` (tests do this via `importlib`)

**What it does**: walks a directory (optionally recursive), filters image files, applies an aspect-ratio-preserving resize into a 1024×600 box, writes outputs with a `resized_` prefix. Honors EXIF orientation; catches per-file errors; supports `--dry-run`, `--workers`, `--format`, `--quality`, `--optimize`, `--mode {contain,fit,stretch}`, `--max-pixels`, `-q`/`-v`.

See `README.md` for the full flag reference.

## Development Conventions

- **Single-file module** — `resize_images.py` is the entire implementation. No internal package structure.
- **Aspect ratio is preserved by default** — `--mode contain` (default) uses `ImageOps.contain`. `--mode stretch` reproduces the original 2022 behavior.
- **Idempotent re-runs** — files starting with `resized_` are skipped, so running the script twice on the same folder is safe.
- **Quality gates** — ruff lint, ruff format, strict mypy, and pytest with a 90% coverage gate. CI runs all four on Linux/macOS/Windows × Python 3.10-3.13.

## How to run

See README.md and CONTRIBUTING.md. Quick reminder for AI agents:

```bash
pip install -r requirements.txt        # runtime
pip install pytest pytest-cov ruff mypy pre-commit  # dev
ruff check . && ruff format --check . && mypy resize_images.py && pytest
```

## Common Tasks for AI Assistants

- **Adding a CLI flag**: edit `parse_args()` in `resize_images.py`, thread the value through `main()` → `resize_directory()`, add a smoke test in `tests/test_resize.py`, update README's flag table.
- **Adding a new image format**: extend the tuple in `_select_targets()` (the `.endswith` check) and the `--format` choices in `parse_args()`.
- **Changing the default size**: edit `DEFAULT_SIZE` in `resize_images.py`. Update README and the test assertions in `tests/test_resize.py` that assert specific output dimensions.
- **Preserving comments and history**: the original `# DIDN'T WORK` comments referencing `ImageOps.pad`/`ImageOps.fit` were intentionally removed when those APIs became part of the actual implementation (issue #4).

## Git Branches

- `main` — stable history.
- `claude/review-clause-md-9u8fk` — large feature branch covering issues #1–#33 (excluding rename-merged history).

## Notes

- Tests load the script via `importlib.util` (see `tests/conftest.py`). This pattern remains in place even after the rename so the suite keeps working if the file is ever renamed again.
- The `format` parameter in `_output_path` and `resize_directory` shadows Python's `format` builtin. This is intentional (it matches Pillow's API) and is silenced via `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml`.
