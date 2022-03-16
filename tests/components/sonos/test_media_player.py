"""Tests for the Sonos Media Player platform."""
from unittest.mock import PropertyMock

import pytest
from soco.exceptions import NotSupportedException

from homeassistant.components.sonos import DATA_SONOS, DOMAIN, media_player
from homeassistant.const import STATE_IDLE
from homeassistant.core import Context
from homeassistant.exceptions import Unauthorized
from homeassistant.helpers import device_registry as dr


async def test_discovery_ignore_unsupported_device(
    hass, async_setup_sonos, soco, caplog
):
    """Test discovery setup."""
    message = f"GetVolume not supported on {soco.ip_address}"
    type(soco).volume = PropertyMock(side_effect=NotSupportedException(message))

    await async_setup_sonos()

    assert message in caplog.text
    assert not hass.data[DATA_SONOS].discovered


async def test_services(hass, async_autosetup_sonos, hass_read_only_user):
    """Test join/unjoin requires control access."""
    with pytest.raises(Unauthorized):
        await hass.services.async_call(
            DOMAIN,
            media_player.SERVICE_JOIN,
            {"master": "media_player.bla", "entity_id": "media_player.blub"},
            blocking=True,
            context=Context(user_id=hass_read_only_user.id),
        )


async def test_device_registry(hass, async_autosetup_sonos, soco):
    """Test sonos device registered in the device registry."""
    device_registry = dr.async_get(hass)
    reg_device = device_registry.async_get_device(
        identifiers={("sonos", "RINCON_test")}
    )
    assert reg_device.model == "Model Name"
    assert reg_device.sw_version == "13.1"
    assert reg_device.connections == {
        (dr.CONNECTION_NETWORK_MAC, "00:11:22:33:44:55"),
        (dr.CONNECTION_UPNP, "uuid:RINCON_test"),
    }
    assert reg_device.manufacturer == "Sonos"
    assert reg_device.suggested_area == "Zone A"
    assert reg_device.name == "Zone A"


async def test_entity_basic(hass, async_autosetup_sonos, discover):
    """Test basic state and attributes."""
    state = hass.states.get("media_player.zone_a")
    assert state.state == STATE_IDLE
    attributes = state.attributes
    assert attributes["friendly_name"] == "Zone A"
    assert attributes["is_volume_muted"] is False
    assert attributes["volume_level"] == 0.19