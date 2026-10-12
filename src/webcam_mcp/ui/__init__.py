"""Bundled MCP App HTML for Webcam Bridge Free controls."""

from importlib import resources
from pathlib import Path

PANEL_URI = "ui://webcam-bridge/panel.html"

# CSP for loading @modelcontextprotocol/ext-apps from unpkg (MCP Apps client SDK).
PANEL_RESOURCE_META = {
    "ui": {
        "csp": {
            "resourceDomains": ["https://unpkg.com"],
        },
        "prefersBorder": True,
    }
}


def load_panel_html() -> str:
    """Return the Free panel HTML (拍一张 / 再拍 / 关掉 + Pro placeholders)."""
    try:
        return resources.files(__package__).joinpath("panel.html").read_text(encoding="utf-8")
    except Exception:
        # Fallback for editable installs / odd loaders
        path = Path(__file__).with_name("panel.html")
        return path.read_text(encoding="utf-8")
