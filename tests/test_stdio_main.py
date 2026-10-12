"""Tests for the stdio entry point."""

import pytest

from webcam_mcp.stdio_main import build_config, parse_args

ENV_VARS = [
    "WEBCAM_CAMERA_INDEX",
    "WEBCAM_PHOTO_WIDTH",
    "WEBCAM_PHOTO_HEIGHT",
    "WEBCAM_VIDEO_WIDTH",
    "WEBCAM_VIDEO_HEIGHT",
]


@pytest.fixture(autouse=True)
def clear_webcam_env(monkeypatch):
    """Keep the ambient environment from leaking into these tests."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_stdio_defaults():
    config = build_config(parse_args([]))

    assert config.camera_index == 0
    assert config.photo_width == 1920
    assert config.photo_height == 1080
    assert config.video_width == 640
    assert config.video_height == 480


def test_stdio_flags_override_defaults():
    config = build_config(
        parse_args(
            [
                "--camera-index",
                "2",
                "--photo-width",
                "1280",
                "--photo-height",
                "720",
                "--video-width",
                "800",
                "--video-height",
                "600",
            ]
        )
    )

    assert config.camera_index == 2
    assert config.photo_width == 1280
    assert config.photo_height == 720
    assert config.video_width == 800
    assert config.video_height == 600


def test_stdio_env_fallback(monkeypatch):
    monkeypatch.setenv("WEBCAM_CAMERA_INDEX", "3")
    monkeypatch.setenv("WEBCAM_PHOTO_WIDTH", "1024")

    config = build_config(parse_args([]))

    assert config.camera_index == 3
    assert config.photo_width == 1024


def test_stdio_flags_win_over_env(monkeypatch):
    monkeypatch.setenv("WEBCAM_CAMERA_INDEX", "3")

    config = build_config(parse_args(["--camera-index", "1"]))

    assert config.camera_index == 1


def test_stdio_invalid_env_falls_back(monkeypatch):
    monkeypatch.setenv("WEBCAM_CAMERA_INDEX", "not-a-number")

    config = build_config(parse_args([]))

    assert config.camera_index == 0
