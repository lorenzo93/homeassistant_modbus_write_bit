"""Support for Modbus."""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import TYPE_CHECKING

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.modbus import (
    get_hub,
)
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_WRITE_REGISTER,
    DEFAULT_HUB,
)

from .const import (
    ATTR_ADDRESS,
    ATTR_BIT_NUMB,
    ATTR_BIT_VALUE,
    ATTR_HUB,
    ATTR_SLAVE,
    SERVICE_WRITE_BIT,
)
from .const import (
    MODBUS_DOMAIN as DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.components.modbus.modbus import ModbusHub
    from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)
_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)


async def async_modbus_bits_setup(hass: HomeAssistant) -> bool:
    """Set up Modbus Write Bit component."""

    async def async_write_bit(service: ServiceCall) -> None:
        """Write Modbus bit."""
        slave = int(float(service.data[ATTR_SLAVE]))
        address = service.data[ATTR_ADDRESS]
        bit_numb = service.data[ATTR_BIT_NUMB]
        bit_value: bool = service.data[ATTR_BIT_VALUE]

        hub_name = service.data.get(ATTR_HUB, DEFAULT_HUB)
        hub: ModbusHub = get_hub(hass, hub_name)

        async with _locks[hub_name]:
            result = await hub.async_pb_call(slave, address, 1, CALL_TYPE_REGISTER_HOLDING)
            if result is None or result.isError():
                _LOGGER.error("Modbus read failed for register %s on hub %s", address, hub_name)
                return

            value = int(result.registers[0])

            if bit_value:
                value |= 1 << bit_numb
            else:
                value &= ~(1 << bit_numb)

            value &= 0xFFFF

            await hub.async_pb_call(slave, address, int(float(value)), CALL_TYPE_WRITE_REGISTER)

    hass.services.async_register(
        DOMAIN,
        SERVICE_WRITE_BIT,
        async_write_bit,
        schema=vol.Schema(
            {
                vol.Optional(ATTR_HUB, default=DEFAULT_HUB): cv.string,
                vol.Exclusive(ATTR_SLAVE, "unit"): vol.All(cv.positive_int, vol.Range(min=0, max=255)),
                vol.Required(ATTR_ADDRESS): vol.All(cv.positive_int, vol.Range(min=0, max=65535)),
                vol.Required(ATTR_BIT_NUMB): vol.All(cv.positive_int, vol.Range(min=0, max=15)),
                vol.Required(ATTR_BIT_VALUE): cv.boolean,
            }
        ),
    )

    return True
