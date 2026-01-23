"""Constants for the MCP Assist integration."""
from __future__ import annotations

from enum import StrEnum


class ServerType(StrEnum):
    """LLM server types supported by MCP Assist."""

    LMSTUDIO = "lmstudio"
    LLAMACPP = "llamacpp"
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"


class ResponseMode(StrEnum):
    """Response/follow-up modes for conversation behavior."""

    NONE = "none"
    DEFAULT = "default"
    ALWAYS = "always"


class SearchProvider(StrEnum):
    """Search providers for web search functionality."""

    NONE = "none"
    BRAVE = "brave"
    DUCKDUCKGO = "duckduckgo"


# Domain constants
DOMAIN = "mcp_assist"
SYSTEM_ENTRY_UNIQUE_ID = "mcp_assist_system_settings"

# Legacy server type constants (deprecated, use ServerType enum)
SERVER_TYPE_LMSTUDIO = ServerType.LMSTUDIO
SERVER_TYPE_LLAMACPP = ServerType.LLAMACPP
SERVER_TYPE_OLLAMA = ServerType.OLLAMA
SERVER_TYPE_OPENAI = ServerType.OPENAI
SERVER_TYPE_GEMINI = ServerType.GEMINI
SERVER_TYPE_ANTHROPIC = ServerType.ANTHROPIC
SERVER_TYPE_OPENROUTER = ServerType.OPENROUTER

# Configuration keys
CONF_PROFILE_NAME = "profile_name"
CONF_SERVER_TYPE = "server_type"
CONF_API_KEY = "api_key"
CONF_LMSTUDIO_URL = "lmstudio_url"
CONF_MODEL_NAME = "model_name"
CONF_MCP_PORT = "mcp_port"
CONF_AUTO_START = "auto_start"
CONF_SYSTEM_PROMPT = "system_prompt"
CONF_TECHNICAL_PROMPT = "technical_prompt"
CONF_CONTROL_HA = "control_home_assistant"
CONF_RESPONSE_MODE = "response_mode"
CONF_FOLLOW_UP_MODE = "follow_up_mode"  # Keep for backward compatibility
CONF_TEMPERATURE = "temperature"
CONF_MAX_TOKENS = "max_tokens"
CONF_MAX_HISTORY = "max_history"
CONF_MAX_ITERATIONS = "max_iterations"
CONF_DEBUG_MODE = "debug_mode"
CONF_ENABLE_CUSTOM_TOOLS = "enable_custom_tools"
CONF_BRAVE_API_KEY = "brave_api_key"
CONF_ALLOWED_IPS = "allowed_ips"
CONF_SEARCH_PROVIDER = "search_provider"
CONF_ENABLE_GAP_FILLING = "enable_gap_filling"
CONF_OLLAMA_KEEP_ALIVE = "ollama_keep_alive"
CONF_OLLAMA_NUM_CTX = "ollama_num_ctx"
CONF_ENABLE_PRE_RESOLVE = "enable_pre_resolve"
CONF_PRE_RESOLVE_THRESHOLD = "pre_resolve_threshold"
CONF_PRE_RESOLVE_MARGIN = "pre_resolve_margin"
CONF_ENABLE_FAST_PATH = "enable_fast_path"
CONF_FAST_PATH_LANGUAGE = "fast_path_language"
CONF_ENABLE_PARALLEL_TOOLS = "enable_parallel_tools"
CONF_FOLLOW_UP_PHRASES = "follow_up_phrases"
CONF_END_WORDS = "end_words"

# Default values
DEFAULT_SERVER_TYPE = ServerType.LMSTUDIO
DEFAULT_LMSTUDIO_URL = "http://localhost:1234"
DEFAULT_LLAMACPP_URL = "http://localhost:8080"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MCP_PORT = 8090
DEFAULT_API_KEY = ""

# Cloud provider base URLs
OPENAI_BASE_URL = "https://api.openai.com"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
ANTHROPIC_BASE_URL = "https://api.anthropic.com"
OPENROUTER_BASE_URL = "https://openrouter.ai/api"

# No hardcoded model lists - models are fetched dynamically from provider APIs
DEFAULT_MODEL_NAME = "model"
DEFAULT_SYSTEM_PROMPT = "You are a helpful Home Assistant voice assistant. Respond naturally and conversationally to user requests."
DEFAULT_CONTROL_HA = True
DEFAULT_RESPONSE_MODE = ResponseMode.DEFAULT
DEFAULT_FOLLOW_UP_MODE = ResponseMode.DEFAULT  # Keep for backward compatibility
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKENS = 500
DEFAULT_MAX_HISTORY = 10
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_DEBUG_MODE = False
DEFAULT_ENABLE_CUSTOM_TOOLS = False
DEFAULT_BRAVE_API_KEY = ""
DEFAULT_ALLOWED_IPS = ""
DEFAULT_SEARCH_PROVIDER = SearchProvider.NONE
DEFAULT_ENABLE_GAP_FILLING = True
DEFAULT_OLLAMA_KEEP_ALIVE = "5m"  # 5 minutes
DEFAULT_OLLAMA_NUM_CTX = 0  # 0 = use model default
DEFAULT_ENABLE_PRE_RESOLVE = True  # Enable entity pre-resolution by default
DEFAULT_PRE_RESOLVE_THRESHOLD = 0.90  # Minimum similarity score for fuzzy matching
DEFAULT_PRE_RESOLVE_MARGIN = 0.08  # Minimum margin to second-best match
DEFAULT_ENABLE_FAST_PATH = True  # Enable Fast Path for simple commands
DEFAULT_FAST_PATH_LANGUAGE = "auto"  # Auto-detect language from HA config
DEFAULT_ENABLE_PARALLEL_TOOLS = True  # Enable parallel tool execution
DEFAULT_FOLLOW_UP_PHRASES = "anything else, what else, would you, do you, should i, can i, which, how can, what about, is there"
DEFAULT_END_WORDS = "stop, cancel, no, nope, thanks, thank you, bye, goodbye, done, never mind, nevermind, forget it, that's all, that's it"

# MCP Server settings
MCP_SERVER_NAME = "ha-entity-discovery"
MCP_PROTOCOL_VERSION = "2024-11-05"

# Entity discovery limits
MAX_ENTITIES_PER_DISCOVERY = 50
MAX_DISCOVERY_RESULTS = 100

# Log sanitization limits
LOG_MAX_RESPONSE_LENGTH = 500
LOG_MAX_TOOL_OUTPUT_LENGTH = 200

# Entity matching limits
ENTITY_MATCH_CHECK_CHARS = 200
ENTITY_INDEX_MAX_SAMPLES = 100

RESPONSE_MODE_INSTRUCTIONS = {
    "none": """## Follow-up Questions
Do NOT ask follow-up questions. Complete the task and end immediately.

## Ending Conversations
Always end after completing the task.""",

    "default": """## Follow-up Questions
Generate contextually appropriate follow-up questions naturally:
- After single device actions: Create a natural follow-up asking if the user needs help with anything else (vary phrasing each time)
- When reporting adjustable status: Spontaneously suggest adjusting it in a natural way
- For partial completions: Ask if the user wants you to complete the remaining tasks
Always vary your phrasing - never repeat the same question twice in a conversation.

Do NOT ask generic "anything else?" or "can I help with anything else?" questions without specific context.
When asking a question, use the set_conversation_state tool to indicate you're expecting a response.

## Ending Conversations
After completing the task, end the conversation unless a natural follow-up is relevant.""",

    "always": """## Follow-up Questions
Generate contextually appropriate follow-up questions naturally:
- After single device actions: Create a natural follow-up asking if the user needs help with anything else (vary phrasing each time)
- When reporting adjustable status: Spontaneously suggest adjusting it in a natural way
- For partial completions: Ask if the user wants you to complete the remaining tasks
Always vary your phrasing - never repeat the same question twice in a conversation.
When asking a question, use the set_conversation_state tool to indicate you're expecting a response.

## Ending Conversations
When user indicates they're done, acknowledge and end naturally."""
}

DEFAULT_TECHNICAL_PROMPT = """You are controlling a Home Assistant smart home system. You have access to sensors, lights, switches, and other devices throughout the home.

## CRITICAL RULES
**Never guess entity IDs.** For ANY device-related request, you MUST:
- FIRST check if [Pre-resolved entities: ...] is provided in the system message
- If pre-resolved entities are available: Use those entity_ids DIRECTLY with perform_action or get_entity_details
- If NO pre-resolved entities: Call discover_entities first to find the actual entities
- This applies EVERY TIME - even for follow-up questions about different entities

## Pre-resolved Entities
When the user message contains `[Pre-resolved entities: "name" = entity_id]`:
- These are already verified entity IDs matching the user's request
- Use them DIRECTLY without calling discover_entities
- Example: User says "Turn on the kitchen light" with `[Pre-resolved entities: "kitchen light" = light.kitchen]`
  → Call perform_action(entity_id="light.kitchen", action="turn_on") immediately
- Multiple entities may be pre-resolved for requests involving several devices

## Available Tools
- **discover_entities**: find devices by name/area/domain/device_class/state (use as FALLBACK if no pre-resolved entities available or mathching)
- **perform_action**: control devices using discovered entity IDs
- **get_entity_details**: check states using discovered entity IDs
- **list_areas/list_domains**: list available areas and device types
- **run_script**: execute scripts that return data (e.g., camera analysis, calculations)
- **run_automation**: trigger automations manually
- **set_conversation_state**: indicate if expecting user response
- **search**: search the web for current information
- **read_url**: read and extract content from web pages

## Scripts (use run_script tool)
Scripts can perform complex operations and return data. Check the index for available scripts with their parameters.

Example - Camera analysis:
  run_script(script_id="llm_camera_analysis", variables={{"camera_entities": "camera.living_room", "prompt": "Is anyone there?"}})

## Automations (use run_automation tool)
Trigger automations manually. Check the index for available automations.

Example:
  run_automation(automation_id="alert_letterbox")

## Discovery Strategy
Use the index below to see what device_classes and domains exist, then query accordingly.

For ANY device request:
1. Check if pre-resolved entities are provided → use them directly
2. If not, check the index to understand what's available
3. Use discover_entities with appropriate filters (device_class, area, domain, name_contains, state)
4. If no results, try broader search

## Response Rules
- Short, concise replies in plain text only (no *, **, markup, or URLs)
- Use Friendly Names (e.g., "Living Room Light"), never entity IDs
- Use natural language for states ("on" → "turned on", "home" → "at home")

{response_mode}

## Index
{index}

Current area: {current_area}
Current time: {time}
Current date: {date}"""


# Public API exports
__all__ = [
    # Enums
    "ServerType",
    "ResponseMode",
    "SearchProvider",
    # Domain
    "DOMAIN",
    "SYSTEM_ENTRY_UNIQUE_ID",
    # Server types (legacy, use ServerType enum)
    "SERVER_TYPE_LMSTUDIO",
    "SERVER_TYPE_LLAMACPP",
    "SERVER_TYPE_OLLAMA",
    "SERVER_TYPE_OPENAI",
    "SERVER_TYPE_GEMINI",
    "SERVER_TYPE_ANTHROPIC",
    "SERVER_TYPE_OPENROUTER",
    # Configuration keys
    "CONF_PROFILE_NAME",
    "CONF_SERVER_TYPE",
    "CONF_API_KEY",
    "CONF_LMSTUDIO_URL",
    "CONF_MODEL_NAME",
    "CONF_MCP_PORT",
    "CONF_AUTO_START",
    "CONF_SYSTEM_PROMPT",
    "CONF_TECHNICAL_PROMPT",
    "CONF_CONTROL_HA",
    "CONF_RESPONSE_MODE",
    "CONF_FOLLOW_UP_MODE",
    "CONF_TEMPERATURE",
    "CONF_MAX_TOKENS",
    "CONF_MAX_HISTORY",
    "CONF_MAX_ITERATIONS",
    "CONF_DEBUG_MODE",
    "CONF_ENABLE_CUSTOM_TOOLS",
    "CONF_BRAVE_API_KEY",
    "CONF_ALLOWED_IPS",
    "CONF_SEARCH_PROVIDER",
    "CONF_ENABLE_GAP_FILLING",
    "CONF_OLLAMA_KEEP_ALIVE",
    "CONF_OLLAMA_NUM_CTX",
    "CONF_ENABLE_PRE_RESOLVE",
    "CONF_PRE_RESOLVE_THRESHOLD",
    "CONF_PRE_RESOLVE_MARGIN",
    "CONF_ENABLE_FAST_PATH",
    "CONF_FAST_PATH_LANGUAGE",
    "CONF_ENABLE_PARALLEL_TOOLS",
    "CONF_FOLLOW_UP_PHRASES",
    "CONF_END_WORDS",
    # Default values
    "DEFAULT_SERVER_TYPE",
    "DEFAULT_LMSTUDIO_URL",
    "DEFAULT_LLAMACPP_URL",
    "DEFAULT_OLLAMA_URL",
    "DEFAULT_MCP_PORT",
    "DEFAULT_API_KEY",
    "DEFAULT_MODEL_NAME",
    "DEFAULT_SYSTEM_PROMPT",
    "DEFAULT_CONTROL_HA",
    "DEFAULT_RESPONSE_MODE",
    "DEFAULT_FOLLOW_UP_MODE",
    "DEFAULT_TEMPERATURE",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_MAX_HISTORY",
    "DEFAULT_MAX_ITERATIONS",
    "DEFAULT_DEBUG_MODE",
    "DEFAULT_ENABLE_CUSTOM_TOOLS",
    "DEFAULT_BRAVE_API_KEY",
    "DEFAULT_ALLOWED_IPS",
    "DEFAULT_SEARCH_PROVIDER",
    "DEFAULT_ENABLE_GAP_FILLING",
    "DEFAULT_OLLAMA_KEEP_ALIVE",
    "DEFAULT_OLLAMA_NUM_CTX",
    "DEFAULT_ENABLE_PRE_RESOLVE",
    "DEFAULT_PRE_RESOLVE_THRESHOLD",
    "DEFAULT_PRE_RESOLVE_MARGIN",
    "DEFAULT_ENABLE_FAST_PATH",
    "DEFAULT_FAST_PATH_LANGUAGE",
    "DEFAULT_ENABLE_PARALLEL_TOOLS",
    "DEFAULT_FOLLOW_UP_PHRASES",
    "DEFAULT_END_WORDS",
    # URLs
    "OPENAI_BASE_URL",
    "GEMINI_BASE_URL",
    "ANTHROPIC_BASE_URL",
    "OPENROUTER_BASE_URL",
    # MCP settings
    "MCP_SERVER_NAME",
    "MCP_PROTOCOL_VERSION",
    # Limits
    "MAX_ENTITIES_PER_DISCOVERY",
    "MAX_DISCOVERY_RESULTS",
    "LOG_MAX_RESPONSE_LENGTH",
    "LOG_MAX_TOOL_OUTPUT_LENGTH",
    "ENTITY_MATCH_CHECK_CHARS",
    "ENTITY_INDEX_MAX_SAMPLES",
    # Prompts
    "RESPONSE_MODE_INSTRUCTIONS",
    "DEFAULT_TECHNICAL_PROMPT",
]