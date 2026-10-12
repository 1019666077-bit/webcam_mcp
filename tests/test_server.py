"""Tests for MCP server tool registration and functionality."""

import pytest

from webcam_mcp.config import ServerConfig
from webcam_mcp.server import create_server
from webcam_mcp.ui import PANEL_URI, load_panel_html


@pytest.mark.asyncio
async def test_tool_registration():
    config = ServerConfig()
    server = create_server(config)

    tools = await server.list_tools()
    tool_names = [tool.name for tool in tools]

    assert "webcam_panel" in tool_names
    assert "take_photo" in tool_names
    assert "record_video" in tool_names


@pytest.mark.asyncio
async def test_tool_metadata():
    config = ServerConfig()
    server = create_server(config)

    tools = await server.list_tools()
    tool_dict = {tool.name: tool for tool in tools}

    assert "take_photo" in tool_dict
    take_photo_tool = tool_dict["take_photo"]
    assert take_photo_tool.description is not None
    assert "photo" in take_photo_tool.description.lower()

    assert "record_video" in tool_dict
    record_video_tool = tool_dict["record_video"]
    assert record_video_tool.description is not None
    assert "video" in record_video_tool.description.lower()

    panel = tool_dict["webcam_panel"]
    assert panel.meta is not None
    assert panel.meta.get("ui", {}).get("resourceUri") == PANEL_URI


@pytest.mark.asyncio
async def test_panel_resource():
    config = ServerConfig()
    server = create_server(config)

    resources = await server.list_resources()
    uris = [str(r.uri) for r in resources]
    assert PANEL_URI in uris

    contents = await server.read_resource(PANEL_URI)
    assert contents
    html = contents[0].content
    assert "拍一张" in html
    assert "再拍" in html
    assert "关掉" in html
    assert "text/html;profile=mcp-app" in (contents[0].mime_type or "")
    assert "连拍 · Pro" in html
    assert load_panel_html() == html


def test_server_config_applied():
    config = ServerConfig(
        host="127.0.0.1", port=9000, camera_index=1, photo_width=1280, photo_height=720
    )
    server = create_server(config)

    assert server.settings.host == "127.0.0.1"
    assert server.settings.port == 9000
