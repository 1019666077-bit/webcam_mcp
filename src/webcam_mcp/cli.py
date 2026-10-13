"""Command-line interface for Webcam MCP server."""

import argparse
import ipaddress
import os
import sys

from webcam_mcp import __version__
from webcam_mcp.config import ServerConfig
from webcam_mcp.server import create_server


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="webcam-mcp",
        description="MCP server for webcam access",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Webcam index (default: 0)",
    )

    parser.add_argument(
        "--photo-width",
        type=int,
        default=1920,
        help="Default photo width (default: 1920)",
    )

    parser.add_argument(
        "--photo-height",
        type=int,
        default=1080,
        help="Default photo height (default: 1080)",
    )

    parser.add_argument(
        "--video-width",
        type=int,
        default=640,
        help="Default video width (default: 640)",
    )

    parser.add_argument(
        "--video-height",
        type=int,
        default=480,
        help="Default video height (default: 480)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"webcam-mcp {__version__}",
    )

    return parser.parse_args(args)


def is_loopback_host(host: str) -> bool:
    """Return True when ``host`` only accepts loopback connections.

    Args:
        host: Hostname or IP address string

    Returns:
        True when the host is a loopback address or the ``localhost`` name
    """
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host.strip().lower() == "localhost"


def check_sse_host_safety(host: str) -> None:
    """Guard SSE transport against unauthenticated LAN exposure.

    SSE transport has no authentication, so binding it to a non-loopback
    address lets anyone on the network trigger the webcam. Print a loud
    warning for non-loopback hosts, and refuse to start unless the operator
    explicitly opts in with ``WEBCAM_MCP_ALLOW_LAN=1``.

    Args:
        host: The host address the SSE server will bind to

    Raises:
        SystemExit: When the host is non-loopback and LAN access is not allowed
    """
    if is_loopback_host(host):
        return

    sys.stderr.write(
        "\n"
        "************************************************************\n"
        " WARNING: webcam-mcp SSE is binding to a non-loopback address\n"
        f"          ({host}). SSE transport has NO authentication, so\n"
        "          anyone on the network can trigger your webcam.\n"
        "          Prefer stdio or a loopback host. Set\n"
        "          WEBCAM_MCP_ALLOW_LAN=1 to accept this risk.\n"
        "************************************************************\n"
        "\n"
    )

    if os.environ.get("WEBCAM_MCP_ALLOW_LAN") != "1":
        sys.stderr.write(
            "ERROR: refusing to expose the webcam over the network. "
            "Set WEBCAM_MCP_ALLOW_LAN=1 to override.\n"
        )
        raise SystemExit(1)


def main(args: list[str] | None = None) -> None:
    """Main entry point for the CLI.

    Parses arguments, creates server configuration, and runs the server.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])
    """
    parsed_args = parse_args(args)

    check_sse_host_safety(parsed_args.host)

    config = ServerConfig(
        camera_index=parsed_args.camera_index,
        photo_width=parsed_args.photo_width,
        photo_height=parsed_args.photo_height,
        video_width=parsed_args.video_width,
        video_height=parsed_args.video_height,
        host=parsed_args.host,
        port=parsed_args.port,
    )

    server = create_server(config)
    server.run(transport="sse")


if __name__ == "__main__":
    main()
