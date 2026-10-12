"""Stdio entry point for Webcam MCP server.

Desktop MCP clients (and MCPB bundles) launch servers over stdio instead of
SSE, so this module builds the same FastMCP server as ``webcam_mcp.cli`` but
runs it with ``transport="stdio"``.

Settings come from command-line flags first, then environment variables
(``WEBCAM_CAMERA_INDEX`` and friends), then the built-in defaults. The
environment fallback is what lets an MCPB ``user_config`` option reach the
server, since MCPB passes user settings as environment variables.
"""

import argparse
import os
import sys
from pathlib import Path

# When this file is executed directly (the MCPB entry point runs it as a
# script), the parent of the package is not on sys.path yet.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from webcam_mcp import __version__  # noqa: E402
from webcam_mcp.config import ServerConfig  # noqa: E402
from webcam_mcp.server import create_server  # noqa: E402


def _env_int(name: str, default: int) -> int:
    """Read an integer setting from the environment.

    Args:
        name: Environment variable name
        default: Value to use when the variable is unset or not an integer

    Returns:
        The parsed integer, or ``default`` when parsing is not possible
    """
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the stdio server.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="webcam-mcp-stdio",
        description="MCP server for webcam access, over stdio",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=None,
        help="Webcam index (default: 0, env: WEBCAM_CAMERA_INDEX)",
    )

    parser.add_argument(
        "--photo-width",
        type=int,
        default=None,
        help="Default photo width (default: 1920, env: WEBCAM_PHOTO_WIDTH)",
    )

    parser.add_argument(
        "--photo-height",
        type=int,
        default=None,
        help="Default photo height (default: 1080, env: WEBCAM_PHOTO_HEIGHT)",
    )

    parser.add_argument(
        "--video-width",
        type=int,
        default=None,
        help="Default video width (default: 640, env: WEBCAM_VIDEO_WIDTH)",
    )

    parser.add_argument(
        "--video-height",
        type=int,
        default=None,
        help="Default video height (default: 480, env: WEBCAM_VIDEO_HEIGHT)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"webcam-mcp {__version__}",
    )

    return parser.parse_args(args)


def build_config(parsed_args: argparse.Namespace) -> ServerConfig:
    """Build a ServerConfig from flags, falling back to the environment.

    Args:
        parsed_args: Parsed command-line arguments (unset flags are None)

    Returns:
        Server configuration for stdio transport
    """
    defaults = ServerConfig()

    def resolve(flag: int | None, env_name: str, fallback: int) -> int:
        if flag is not None:
            return flag
        return _env_int(env_name, fallback)

    return ServerConfig(
        camera_index=resolve(parsed_args.camera_index, "WEBCAM_CAMERA_INDEX", defaults.camera_index),
        photo_width=resolve(parsed_args.photo_width, "WEBCAM_PHOTO_WIDTH", defaults.photo_width),
        photo_height=resolve(
            parsed_args.photo_height, "WEBCAM_PHOTO_HEIGHT", defaults.photo_height
        ),
        video_width=resolve(parsed_args.video_width, "WEBCAM_VIDEO_WIDTH", defaults.video_width),
        video_height=resolve(
            parsed_args.video_height, "WEBCAM_VIDEO_HEIGHT", defaults.video_height
        ),
    )


def main(args: list[str] | None = None) -> None:
    """Run the Webcam MCP server over stdio.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])
    """
    config = build_config(parse_args(args))

    server = create_server(config)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
