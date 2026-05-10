# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `argparse` CLI: pass the target folder as a positional argument instead of editing the script. (#1)
- `--mode {contain,fit,stretch}` flag controlling aspect-ratio behavior. Default is `contain`, which finally honors the README's "Keeping it aspect ratio" claim. (#4)
- `-r`/`--recursive` to walk subdirectories. (#22)
- `--format` to convert outputs to JPEG, PNG, WebP, BMP, or TIFF. (#23)
- `--dry-run` to preview targets without writing. (#26)
- `--quality` and `--optimize` flags forwarded to Pillow's encoder. (#27)
- `--max-pixels` to override Pillow's decompression-bomb threshold (or disable it with `0`). (#6)
- `--workers N` for parallel processing via `ThreadPoolExecutor`. (#24)
- `-q`/`--quiet` and `-v`/`--verbose` flags; output now goes through `logging`. (#25)
- Progress bar via `tqdm` when installed (optional dependency). (#25)
- `requirements.txt` and `pyproject.toml` with dev extras. (#8, #9)
- Project metadata: MIT `LICENSE`, expanded `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`. (#11, #14, #28, #31, #32, #10)
- GitHub issue templates and PR template. (#29, #30)
- GitHub Actions CI matrix across Linux/macOS/Windows × Python 3.10-3.13 running ruff lint, ruff format, mypy, and pytest. (#16)
- Dependabot configuration for weekly dep updates. (#33)
- Pre-commit hooks for ruff, mypy, and standard hygiene checks. (#21)
- pytest test suite with `pytest-cov` and a 90% coverage gate. (#15, #17)
- Strict mypy configuration. (#20)
- ruff lint and format configurations. (#18, #19)

### Changed

- Filenames are now matched case-insensitively, so `.JPG`, `.PNG`, `.JPEG` are picked up. (#2)
- Files already starting with `resized_` are skipped, making re-runs idempotent. (#3)
- EXIF orientation is honored before resizing — phone photos no longer come out sideways. (#7)
- Per-file errors (corrupt files, decompression bombs) are logged as warnings; the batch continues. (#5)

### Removed

- Unused `import PIL` line. (#13)
- Obsolete `# DIDN'T WORK` comments referencing `ImageOps.pad` / `ImageOps.fit` (these are now used deliberately as part of `--mode`). (#4)

[Unreleased]: https://github.com/thiagobra/Resize-all-Images-in-a-folder/compare/HEAD
