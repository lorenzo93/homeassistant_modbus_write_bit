# Homeassistant Modbus Write Bit integration

Homeassistant integration for writing a single bit to a Modbus register.


## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
1. Download _all_ the files from the `custom_components/modbus_write_bit/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Modbus Innova"

## Configuration is done in the configuration.yaml file

1. Configure the modbus integration with the correct data.
1. Load the `modbus_write_bit` integration by just writing a line into the `configuration.yaml`

```yaml
modbus:
  - name: modbus_hub
    type: tcp
    host: x.y.z.k

modbus_write_bit:
```
1. Use the integration in an action
```yaml
action: modbus_write_bit.write_bit
data:
  address: <target register address>
  slave: <target slave address>
  hub: <hub name>
  bit_numb: <bit number to change>
  bit_value: <0 or 1>
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)