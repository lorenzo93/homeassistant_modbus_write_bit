"""Support for Modbus."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.modbus import (
    CALL_TYPE_REGISTER_HOLDING,
    DEFAULT_HUB,
    ModbusHub,
    get_hub,
)
from homeassistant.components.modbus.const import CALL_TYPE_WRITE_REGISTER

from .const import (
    ATTR_ADDRESS,
    ATTR_BIT_NUMB,
    ATTR_BIT_VALUE,
    ATTR_HUB,
    ATTR_SLAVE,
    ATTR_UNIT,
    SERVICE_WRITE_BIT,
)
from .const import (
    MODBUS_DOMAIN as DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall
    from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)


async def async_modbus_bits_setup(
    hass: HomeAssistant,
    config: ConfigType,
) -> bool:
    """Set up Modbus component."""

    async def async_write_bit(service: ServiceCall) -> None:
        """Write Modbus bit."""
        slave = 0
        if ATTR_UNIT in service.data:
            slave = int(float(service.data[ATTR_UNIT]))
        if ATTR_SLAVE in service.data:
            slave = int(float(service.data[ATTR_SLAVE]))
        address = service.data[ATTR_ADDRESS]
        bit_numb = service.data[ATTR_BIT_NUMB]
        bit_value: bool = service.data[ATTR_BIT_VALUE]
        hub: ModbusHub = get_hub(hass, service.data.get(ATTR_HUB, DEFAULT_HUB))

        result = await hub.async_pb_call(slave, address, 1, CALL_TYPE_REGISTER_HOLDING)
        value = int(result.registers[0])

        if bit_value:
            value |= 1 << bit_numb
        else:
            value &= ~(1 << bit_numb)

        await hub.async_pb_call(
            slave, address, int(float(value)), CALL_TYPE_WRITE_REGISTER
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_WRITE_BIT,
        async_write_bit,
        schema=vol.Schema(
            {
                vol.Optional(ATTR_HUB, default=DEFAULT_HUB): cv.string,
                vol.Exclusive(ATTR_SLAVE, "unit"): cv.positive_int,
                vol.Exclusive(ATTR_UNIT, "unit"): cv.positive_int,
                vol.Required(ATTR_ADDRESS): cv.positive_int,
                vol.Required(ATTR_BIT_NUMB): cv.positive_int,
                vol.Required(ATTR_BIT_VALUE): cv.boolean,
            }
        ),
    )

    return True
