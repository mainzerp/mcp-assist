"""Custom exceptions for MCP Assist integration."""
from __future__ import annotations


class MCPAssistError(Exception):
    """Base exception for MCP Assist errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            details: Optional technical details for debugging
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation."""
        if self.details:
            return f"{self.message} ({self.details})"
        return self.message


class LLMConnectionError(MCPAssistError):
    """Error connecting to LLM provider."""


class LLMResponseError(MCPAssistError):
    """Error in LLM response parsing or processing."""


class ToolExecutionError(MCPAssistError):
    """Error executing an MCP tool."""

    def __init__(
        self,
        message: str,
        tool_name: str | None = None,
        details: str | None = None
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            tool_name: Name of the tool that failed
            details: Optional technical details
        """
        super().__init__(message, details)
        self.tool_name = tool_name


class EntityResolutionError(MCPAssistError):
    """Error resolving entity names to entity IDs."""

    def __init__(
        self,
        message: str,
        entity_name: str | None = None,
        suggestions: list[str] | None = None,
        details: str | None = None
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            entity_name: The entity name that could not be resolved
            suggestions: List of similar entity names as alternatives
            details: Optional technical details
        """
        super().__init__(message, details)
        self.entity_name = entity_name
        self.suggestions = suggestions or []


class ConfigurationError(MCPAssistError):
    """Error in integration configuration."""


class MCPServerError(MCPAssistError):
    """Error in MCP server operations."""


class ValidationError(MCPAssistError):
    """Error validating input data."""


__all__ = [
    "MCPAssistError",
    "LLMConnectionError",
    "LLMResponseError",
    "ToolExecutionError",
    "EntityResolutionError",
    "ConfigurationError",
    "MCPServerError",
    "ValidationError",
]
