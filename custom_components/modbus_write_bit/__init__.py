"""Support for Modbus."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .const import (
    MODBUS_DOMAIN as DOMAIN,
)
from .modbus import async_modbus_bits_setup

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Modbus component."""
    if DOMAIN not in config:
        return False
    return await async_modbus_bits_setup(hass)
