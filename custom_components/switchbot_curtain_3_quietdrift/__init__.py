"""QuietDrift support for SwitchBot Curtain devices."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_registry
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID

from .const import (
    CONF_SPEED, 
    CONF_POSITION, 
    DOMAIN, 
    SET_COVER_POSITION_SCHEMA,
    SPEED_QUIETDRIFT,
    SPEED_SILENT,
    SPEED_NORMAL
)

_LOGGER = logging.getLogger(__name__)

# Map readable names to actual integer speeds
SPEED_MAP = {
    SPEED_QUIETDRIFT: 1,    # QuietDrift
    SPEED_SILENT: 2,        # Silent
    SPEED_NORMAL: 255       # Normal
}

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry (UI)."""

    async def handle_set_cover_position(service_call: ServiceCall):
        data = service_call.data
        
        # Get string value (e.g., "QuietDrift")
        speed_key = data[CONF_SPEED]
        # Convert to integer (e.g., 1)
        speed = SPEED_MAP.get(speed_key, 255)
        
        position = data[CONF_POSITION]
        entity_ids = data[CONF_ENTITY_ID]

        ent_reg = entity_registry.async_get(hass)
        
        entities = []
        for eid in entity_ids:
            reg_entry = ent_reg.async_get(eid)
            if reg_entry:
                cover_data = hass.data.get('cover')
                if cover_data:
                    entity = cover_data.get_entity(eid)
                    if entity:
                        entities.append(entity)
        
        for entity in entities:
            try:
                if not hasattr(entity, '_device'):
                    _LOGGER.warning(f"Entity {entity.entity_id} missing _device attribute")
                    continue

                res = await entity._device.set_position(position=position, speed=speed)
                
                (_LOGGER.info if res else _LOGGER.warning)(
                    'set position (%s, %d, %d) result: %s', 
                    entity.entity_id, position, speed, res
                )

                entity._last_run_success = bool(res)
                entity._attr_is_opening = entity._device.is_opening()
                entity._attr_is_closing = entity._device.is_closing()
                entity.async_write_ha_state()

            except Exception as e:
                _LOGGER.error(f"Error handling {entity.entity_id}: {e}")

    hass.services.async_register(
        domain=DOMAIN,
        service='set_switchbot_curtain_position',
        service_func=handle_set_cover_position,
        schema=SET_COVER_POSITION_SCHEMA,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.services.async_remove(DOMAIN, 'set_switchbot_curtain_position')
    return True
