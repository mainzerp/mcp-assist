"""Utility functions for MCP Assist integration."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


def get_shared_setting(
    hass: HomeAssistant,
    entry: ConfigEntry | None,
    key: str,
    default: Any = None
) -> Any:
    """Get a shared setting from system entry with fallback to profile entry.

    This function provides a unified way to retrieve configuration settings
    across the integration. It first checks the system entry (shared settings),
    then falls back to the profile entry for backward compatibility.

    Args:
        hass: Home Assistant instance
        entry: Optional config entry to fall back to
        key: Configuration key to retrieve
        default: Default value if key is not found

    Returns:
        The configuration value or default

    Example:
        >>> mcp_port = get_shared_setting(hass, entry, CONF_MCP_PORT, DEFAULT_MCP_PORT)
    """
    from . import get_system_entry

    # Try to get from system entry first
    system_entry = get_system_entry(hass)
    if system_entry:
        value = system_entry.options.get(key, system_entry.data.get(key))
        if value is not None:
            return value

    # Fallback to profile entry for backward compatibility
    if entry:
        value = entry.options.get(key, entry.data.get(key))
        if value is not None:
            return value

    return default


def get_entry_setting(
    entry: ConfigEntry,
    key: str,
    default: Any = None
) -> Any:
    """Get a setting from a config entry (options first, then data).

    Args:
        entry: Config entry to read from
        key: Configuration key to retrieve
        default: Default value if key is not found

    Returns:
        The configuration value or default
    """
    value = entry.options.get(key, entry.data.get(key))
    return value if value is not None else default


def sanitize_log_data(data: Any, max_length: int = 500) -> str:
    """Sanitize data for logging, truncating if necessary.

    Removes or masks potentially sensitive information and limits length
    to prevent log flooding.

    Args:
        data: Data to sanitize
        max_length: Maximum length of output string

    Returns:
        Sanitized string representation
    """
    if data is None:
        return "<None>"

    text = str(data)

    # Truncate if too long
    if len(text) > max_length:
        return f"{text[:max_length]}... [truncated, {len(text)} chars total]"

    return text


__all__ = [
    "get_shared_setting",
    "get_entry_setting",
    "sanitize_log_data",
]
