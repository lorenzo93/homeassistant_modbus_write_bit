"""Constants used in modbus_bits integration."""

from homeassistant.const import (
    CONF_ADDRESS,
)

# service call attributes
ATTR_ADDRESS = CONF_ADDRESS
ATTR_HUB = "hub"
ATTR_SLAVE = "slave"
ATTR_VALUE = "value"
ATTR_BIT_NUMB = "bit_numb"
ATTR_BIT_VALUE = "bit_value"

# service calls
SERVICE_WRITE_BIT = "write_bit"

# integration names
MODBUS_DOMAIN = "modbus_write_bit"
