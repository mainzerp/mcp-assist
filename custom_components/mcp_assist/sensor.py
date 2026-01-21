"""Sensor platform for MCP Assist statistics."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfTime, EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, SYSTEM_ENTRY_UNIQUE_ID

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class MCPAssistSensorDescription(SensorEntityDescription):
    """Describes MCP Assist sensor entity."""

    value_fn: Callable[[dict], Any] = lambda x: None
    attr_fn: Callable[[dict, Any], dict] | None = None


SENSOR_TYPES: tuple[MCPAssistSensorDescription, ...] = (
    # Status
    MCPAssistSensorDescription(
        key="status",
        translation_key="status",
        name="Status",
        icon="mdi:check-network",
        value_fn=lambda stats: stats.get("status", "unknown"),
        attr_fn=lambda stats, _: {
            "last_request": stats.get("last_request_time"),
        },
    ),
    # Fast Path Response Times
    MCPAssistSensorDescription(
        key="fast_path_avg_response_time",
        translation_key="fast_path_avg_response_time",
        name="Fast Path Avg Response Time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:lightning-bolt",
        value_fn=lambda stats: stats.get("fast_path_avg_response_time", 0),
    ),
    # LLM Response Times
    MCPAssistSensorDescription(
        key="llm_avg_response_time",
        translation_key="llm_avg_response_time",
        name="LLM Avg Response Time",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:robot",
        value_fn=lambda stats: stats.get("llm_avg_response_time", 0),
    ),
    # Fast Path Rate
    MCPAssistSensorDescription(
        key="fast_path_rate",
        translation_key="fast_path_rate",
        name="Fast Path Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:percent-circle",
        value_fn=lambda stats: stats.get("fast_path_rate", 0),
        attr_fn=lambda stats, _: {
            "hits": stats.get("fast_path_hits", 0),
            "misses": stats.get("fast_path_misses", 0),
        },
    ),
    # Fast Path Hits
    MCPAssistSensorDescription(
        key="fast_path_hits",
        translation_key="fast_path_hits",
        name="Fast Path Hits",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:lightning-bolt-circle",
        value_fn=lambda stats: stats.get("fast_path_hits", 0),
    ),
    # Pre-Resolve Rate
    MCPAssistSensorDescription(
        key="pre_resolve_rate",
        translation_key="pre_resolve_rate",
        name="Pre-Resolve Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:target",
        value_fn=lambda stats: stats.get("pre_resolve_rate", 0),
        attr_fn=lambda stats, _: {
            "hits": stats.get("pre_resolve_hits", 0),
            "attempts": stats.get("pre_resolve_attempts", 0),
        },
    ),
    # LLM Calls Today
    MCPAssistSensorDescription(
        key="llm_calls_today",
        translation_key="llm_calls_today",
        name="LLM Calls Today",
        state_class=SensorStateClass.TOTAL,
        icon="mdi:robot-outline",
        value_fn=lambda stats: stats.get("llm_calls_today", 0),
        attr_fn=lambda stats, _: {
            "total": stats.get("llm_calls_total", 0),
        },
    ),
    # Tokens Used Today
    MCPAssistSensorDescription(
        key="tokens_used_today",
        translation_key="tokens_used_today",
        name="Tokens Used Today",
        state_class=SensorStateClass.TOTAL,
        icon="mdi:code-tags",
        value_fn=lambda stats: stats.get("tokens_used_today", 0),
        attr_fn=lambda stats, _: {
            "total": stats.get("tokens_used_total", 0),
        },
    ),
    # Requests Today
    MCPAssistSensorDescription(
        key="requests_today",
        translation_key="requests_today",
        name="Requests Today",
        state_class=SensorStateClass.TOTAL,
        icon="mdi:message-text",
        value_fn=lambda stats: stats.get("requests_today", 0),
    ),
    # Indexed Entities
    MCPAssistSensorDescription(
        key="indexed_entities",
        translation_key="indexed_entities",
        name="Indexed Entities",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda stats: stats.get("indexed_entities", 0),
    ),
    # LLM Errors
    MCPAssistSensorDescription(
        key="llm_errors",
        translation_key="llm_errors",
        name="LLM Errors",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda stats: stats.get("llm_errors", 0),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MCP Assist sensors from a config entry."""
    # Only create sensors once (for system entry or first profile)
    if entry.unique_id == SYSTEM_ENTRY_UNIQUE_ID:
        _LOGGER.debug("Skipping sensor setup for system entry")
        return

    # Check if sensors already exist
    if hass.data.get(DOMAIN, {}).get("sensors_created"):
        _LOGGER.debug("Sensors already created, skipping")
        return

    # Get statistics manager
    stats_manager = hass.data.get(DOMAIN, {}).get("statistics")
    if not stats_manager:
        _LOGGER.warning("Statistics manager not available, skipping sensor setup")
        return

    # Get index manager for indexed_entities count
    index_manager = hass.data.get(DOMAIN, {}).get("index_manager")

    # Mark sensors as created
    hass.data[DOMAIN]["sensors_created"] = True

    entities = [
        MCPAssistSensor(hass, entry, description, stats_manager, index_manager)
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)
    _LOGGER.info("Created %d MCP Assist sensors", len(entities))


class MCPAssistSensor(SensorEntity):
    """Representation of a MCP Assist sensor."""

    entity_description: MCPAssistSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: MCPAssistSensorDescription,
        stats_manager,
        index_manager,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.entity_description = description
        self._stats_manager = stats_manager
        self._index_manager = index_manager
        self._attr_unique_id = f"mcp_assist_{description.key}"
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, "mcp_assist_stats")},
            name="MCP Assist Statistics",
            manufacturer="MCP Assist",
            model="Statistics",
            entry_type=dr.DeviceEntryType.SERVICE,
        )
        self._remove_listener: Callable[[], None] | None = None

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()

        # Register for statistics updates
        @callback
        def _stats_updated():
            """Handle stats update."""
            self.async_write_ha_state()

        self._remove_listener = self._stats_manager.add_listener(_stats_updated)

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        if self._remove_listener:
            self._remove_listener()
            self._remove_listener = None

        await super().async_will_remove_from_hass()

    def _get_stats(self) -> dict:
        """Get current statistics including index manager data."""
        stats = self._stats_manager.get_stats()

        # Add indexed entities count from index manager
        if self._index_manager:
            entity_names = self._index_manager.get_entity_names()
            if entity_names:
                # Count unique entity_ids
                unique_entities = len(set(entity_names.values()))
                stats["indexed_entities"] = unique_entities

        return stats

    @property
    def native_value(self):
        """Return the state of the sensor."""
        stats = self._get_stats()
        return self.entity_description.value_fn(stats)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional attributes."""
        if self.entity_description.attr_fn:
            stats = self._get_stats()
            return self.entity_description.attr_fn(stats, self.native_value)
        return None
