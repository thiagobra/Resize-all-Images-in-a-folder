# Contributing

Thanks for your interest in improving this project! This is a small utility, so the bar is mostly: keep it simple, keep it tested, keep it cross-platform.

## Setting up

```bash
git clone https://github.com/thiagobra/Resize-all-Images-in-a-folder
cd Resize-all-Images-in-a-folder
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov ruff mypy pre-commit
pre-commit install
```

## Running checks locally

```bash
ruff check .                        # lint
ruff format --check .               # formatting
mypy resize_images.py               # type-check
pytest                              # tests + coverage gate (>=90%)
```

CI runs the same four checks on every push and PR across Linux/macOS/Windows for Python 3.10-3.13.

## Workflow

1. Find or open an issue describing the change.
2. Fork the repository (or use a feature branch if you have push access).
3. Branch from `main`. The convention used by maintainers is `claude/<issue-number>-<short-slug>`, but anything descriptive is fine.
4. Make focused, atomic commits — one logical change per commit, with a `Closes #N` footer where applicable.
5. Open a pull request using the [PR template](.github/PULL_REQUEST_TEMPLATE.md). Make sure CI is green.

## Smoke testing

Before opening a PR, run the script against a fixture folder containing at least one of each:

- a JPEG, a PNG, and a JPEG with `.JPG` extension
- a non-image file with a `.jpg` extension (to exercise the per-file error path)
- (optional) a sub-folder, if your change touches recursion

Verify expected outputs are written and unexpected files aren't modified.

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml). Please include Python version, Pillow version, OS, and a minimal reproduction.

## Security

See [SECURITY.md](SECURITY.md). Please don't open public issues for security problems.
