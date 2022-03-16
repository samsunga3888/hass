"""Support for Abode Security System lights."""
from __future__ import annotations

from math import ceil
from typing import Any

from abodepy.devices.light import AbodeLight as AbodeLT
import abodepy.helpers.constants as CONST

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_HS_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.color import (
    color_temperature_kelvin_to_mired,
    color_temperature_mired_to_kelvin,
)

from . import AbodeDevice, AbodeSystem
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Abode light devices."""
    data: AbodeSystem = hass.data[DOMAIN]

    entities = []

    for device in data.abode.get_devices(generic_type=CONST.TYPE_LIGHT):
        entities.append(AbodeLight(data, device))

    async_add_entities(entities)


class AbodeLight(AbodeDevice, LightEntity):
    """Representation of an Abode light."""

    _device: AbodeLT

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        if ATTR_COLOR_TEMP in kwargs and self._device.is_color_capable:
            self._device.set_color_temp(
                int(color_temperature_mired_to_kelvin(kwargs[ATTR_COLOR_TEMP]))
            )
            return

        if ATTR_HS_COLOR in kwargs and self._device.is_color_capable:
            self._device.set_color(kwargs[ATTR_HS_COLOR])
            return

        if ATTR_BRIGHTNESS in kwargs and self._device.is_dimmable:
            # Convert Home Assistant brightness (0-255) to Abode brightness (0-99)
            # If 100 is sent to Abode, response is 99 causing an error
            self._device.set_level(ceil(kwargs[ATTR_BRIGHTNESS] * 99 / 255.0))
            return

        self._device.switch_on()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        self._device.switch_off()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return bool(self._device.is_on)

    @property
    def brightness(self) -> int | None:
        """Return the brightness of the light."""
        if self._device.is_dimmable and self._device.has_brightness:
            brightness = int(self._device.brightness)
            # Abode returns 100 during device initialization and device refresh
            # Convert Abode brightness (0-99) to Home Assistant brightness (0-255)
            return 255 if brightness == 100 else ceil(brightness * 255 / 99.0)
        return None

    @property
    def color_temp(self) -> int | None:
        """Return the color temp of the light."""
        if self._device.has_color:
            return color_temperature_kelvin_to_mired(self._device.color_temp)
        return None

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the color of the light."""
        _hs = None
        if self._device.has_color:
            _hs = self._device.color
        return _hs

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        if self._device.is_dimmable and self._device.is_color_capable:
            return SUPPORT_BRIGHTNESS | SUPPORT_COLOR | SUPPORT_COLOR_TEMP
        if self._device.is_dimmable:
            return SUPPORT_BRIGHTNESS
        return 0