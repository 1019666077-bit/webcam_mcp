"""Tests for CLI argument parsing."""

import pytest

from webcam_mcp.cli import check_sse_host_safety, is_loopback_host, parse_args


def test_cli_defaults():
    args = parse_args([])

    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.camera_index == 0
    assert args.photo_width == 1920
    assert args.photo_height == 1080
    assert args.video_width == 640
    assert args.video_height == 480


def test_cli_custom_host_port():
    args = parse_args(["--host", "127.0.0.1", "--port", "9000"])

    assert args.host == "127.0.0.1"
    assert args.port == 9000


def test_cli_custom_camera():
    args = parse_args(["--camera-index", "1"])

    assert args.camera_index == 1


def test_cli_custom_photo_resolution():
    args = parse_args(["--photo-width", "1280", "--photo-height", "720"])

    assert args.photo_width == 1280
    assert args.photo_height == 720


def test_cli_custom_video_resolution():
    args = parse_args(["--video-width", "1280", "--video-height", "720"])

    assert args.video_width == 1280
    assert args.video_height == 720


def test_cli_version():
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--version"])

    assert exc_info.value.code == 0


def test_cli_help():
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])

    assert exc_info.value.code == 0


@pytest.mark.parametrize(
    ("host", "expected"),
    [
        ("127.0.0.1", True),
        ("::1", True),
        ("localhost", True),
        ("0.0.0.0", False),
        ("::", False),
        ("192.168.1.5", False),
        ("example.com", False),
    ],
)
def test_is_loopback_host(host, expected):
    assert is_loopback_host(host) is expected


def test_sse_host_safety_allows_loopback():
    check_sse_host_safety("127.0.0.1")
    check_sse_host_safety("localhost")


def test_sse_host_safety_refuses_non_loopback(capsys):
    with pytest.raises(SystemExit) as exc_info:
        check_sse_host_safety("0.0.0.0")

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "WEBCAM_MCP_ALLOW_LAN" in captured.err


def test_sse_host_safety_allows_lan_with_env(monkeypatch, capsys):
    monkeypatch.setenv("WEBCAM_MCP_ALLOW_LAN", "1")

    check_sse_host_safety("0.0.0.0")

    captured = capsys.readouterr()
    assert "non-loopback" in captured.err
