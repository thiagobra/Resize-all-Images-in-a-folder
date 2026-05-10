"""End-to-end tests for the resize script."""

from __future__ import annotations

import pathlib
from types import ModuleType

import pytest
from PIL import Image


def _make_jpg(path: pathlib.Path, size: tuple[int, int] = (400, 400), color: str = "red") -> None:
    Image.new("RGB", size, color).save(path)


def test_default_mode_preserves_aspect_ratio(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg", size=(800, 600))
    script.resize_directory(str(tmp_path))
    out = Image.open(tmp_path / "resized_a.jpg")
    assert out.size == (800, 600)  # contain mode: 800x600 fits inside 1024x600


def test_mixed_case_extensions(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "IMG.JPG")
    Image.new("RGB", (400, 400), "blue").save(tmp_path / "Photo.PNG")
    script.resize_directory(str(tmp_path))
    assert (tmp_path / "resized_IMG.JPG").exists()
    assert (tmp_path / "resized_Photo.PNG").exists()


def test_idempotent_rerun(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.resize_directory(str(tmp_path))
    script.resize_directory(str(tmp_path))
    assert not (tmp_path / "resized_resized_a.jpg").exists()


def test_dry_run_writes_nothing(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.resize_directory(str(tmp_path), dry_run=True)
    assert not (tmp_path / "resized_a.jpg").exists()


def test_corrupt_file_is_skipped(script: ModuleType, tmp_path: pathlib.Path) -> None:
    (tmp_path / "fake.jpg").write_bytes(b"not an image")
    _make_jpg(tmp_path / "good.jpg")
    script.resize_directory(str(tmp_path))
    assert (tmp_path / "resized_good.jpg").exists()
    assert not (tmp_path / "resized_fake.jpg").exists()


def test_recursive(script: ModuleType, tmp_path: pathlib.Path) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    _make_jpg(tmp_path / "top.jpg")
    _make_jpg(sub / "deep.jpg", color="blue")
    script.resize_directory(str(tmp_path), recursive=True)
    assert (tmp_path / "resized_top.jpg").exists()
    assert (sub / "resized_deep.jpg").exists()


def test_non_recursive_skips_subdirs(script: ModuleType, tmp_path: pathlib.Path) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    _make_jpg(sub / "deep.jpg")
    script.resize_directory(str(tmp_path))
    assert not (sub / "resized_deep.jpg").exists()


def test_format_conversion(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.resize_directory(str(tmp_path), format="webp")
    assert (tmp_path / "resized_a.webp").exists()
    assert not (tmp_path / "resized_a.jpg").exists()


def test_stretch_mode_ignores_aspect(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.resize_directory(str(tmp_path), mode="stretch")
    assert Image.open(tmp_path / "resized_a.jpg").size == (1024, 600)


def test_fit_mode_fills_target(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.resize_directory(str(tmp_path), mode="fit")
    assert Image.open(tmp_path / "resized_a.jpg").size == (1024, 600)


def test_invalid_mode_raises(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    with pytest.raises(ValueError, match="unknown mode"):
        script.resize_directory(str(tmp_path), mode="bogus")


def test_workers_runs_to_completion(script: ModuleType, tmp_path: pathlib.Path) -> None:
    for i in range(4):
        _make_jpg(tmp_path / f"img{i}.jpg")
    script.resize_directory(str(tmp_path), workers=2)
    assert sum(1 for p in tmp_path.iterdir() if p.name.startswith("resized_")) == 4


def test_parse_args_defaults(script: ModuleType) -> None:
    args = script.parse_args(["/some/dir"])
    assert args.directory == "/some/dir"
    assert args.mode == "contain"
    assert args.workers == 1
    assert args.recursive is False
    assert args.format is None
    assert args.dry_run is False


def test_parse_args_overrides(script: ModuleType) -> None:
    args = script.parse_args(
        [
            "--mode",
            "fit",
            "-r",
            "--workers",
            "4",
            "--quality",
            "80",
            "--optimize",
            "/dir",
        ]
    )
    assert args.mode == "fit"
    assert args.recursive is True
    assert args.workers == 4
    assert args.quality == 80
    assert args.optimize is True


def test_main_end_to_end(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.main([str(tmp_path)])
    assert (tmp_path / "resized_a.jpg").exists()


def test_main_max_pixels_zero_disables_check(script: ModuleType, tmp_path: pathlib.Path) -> None:
    _make_jpg(tmp_path / "a.jpg")
    script.main(["--max-pixels", "0", str(tmp_path)])
    assert (tmp_path / "resized_a.jpg").exists()
