"""Custom tools loader for MCP Assist."""
from __future__ import annotations

import logging
from typing import Any

from ..utils import get_shared_setting

_LOGGER = logging.getLogger(__name__)


class CustomToolsLoader:
    """Load and manage custom tools."""

    def __init__(self, hass, entry=None):
        """Initialize the custom tools loader."""
        self.hass = hass
        self.entry = entry
        self.tools = {}

    async def initialize(self):
        """Initialize custom tools based on search provider selection."""
        # Determine search provider
        search_provider = self._get_search_provider()

        # Load search tool based on provider
        if search_provider == "brave":
            try:
                from .brave_search import BraveSearchTool
                # Get Brave API key from system entry (shared setting)
                api_key = self._get_brave_api_key()
                self.tools["search"] = BraveSearchTool(self.hass, api_key)
                await self.tools["search"].initialize()
                _LOGGER.debug("Brave Search tool initialized")
            except Exception as e:
                _LOGGER.error("Failed to initialize Brave Search tool: %s", e)

        elif search_provider == "duckduckgo":
            try:
                from .duckduckgo_search import DuckDuckGoSearchTool
                self.tools["search"] = DuckDuckGoSearchTool(self.hass)
                await self.tools["search"].initialize()
                _LOGGER.debug("DuckDuckGo Search tool initialized")
            except Exception as e:
                _LOGGER.error("Failed to initialize DuckDuckGo Search tool: %s", e)

        # Load read_url tool if search is enabled
        if search_provider in ["brave", "duckduckgo"]:
            try:
                from .read_url import ReadUrlTool
                self.tools["read_url"] = ReadUrlTool(self.hass)
                await self.tools["read_url"].initialize()
                _LOGGER.debug("Read URL tool initialized")
            except Exception as e:
                _LOGGER.error("Failed to initialize read_url tool: %s", e)

    def _get_search_provider(self) -> str:
        """Get search provider (shared setting) with backward compatibility."""
        from ..const import CONF_SEARCH_PROVIDER, CONF_ENABLE_CUSTOM_TOOLS

        provider = get_shared_setting(self.hass, self.entry, CONF_SEARCH_PROVIDER)
        if provider:
            return provider

        # Backward compat: if old enable_custom_tools was True, default to "brave"
        if get_shared_setting(self.hass, self.entry, CONF_ENABLE_CUSTOM_TOOLS, False):
            return "brave"

        return "none"

    def _get_brave_api_key(self) -> str:
        """Get Brave API key (shared setting)."""
        from ..const import CONF_BRAVE_API_KEY, DEFAULT_BRAVE_API_KEY
        return get_shared_setting(self.hass, self.entry, CONF_BRAVE_API_KEY, DEFAULT_BRAVE_API_KEY)

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Get MCP tool definitions for all enabled tools."""
        definitions = []
        for tool in self.tools.values():
            try:
                definitions.extend(tool.get_tool_definitions())
            except Exception as e:
                _LOGGER.error("Error getting tool definitions: %s", e)
        return definitions

    async def handle_tool_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Handle a custom tool call."""
        for tool in self.tools.values():
            if tool.handles_tool(tool_name):
                return await tool.handle_call(tool_name, arguments)

        raise ValueError(f"Unknown custom tool: {tool_name}")

    def is_custom_tool(self, tool_name: str) -> bool:
        """Check if a tool name is a custom tool."""
        for tool in self.tools.values():
            if tool.handles_tool(tool_name):
                return True
        return False


__all__ = ["CustomToolsLoader"]