"""The epson integration."""
import logging


from pypjlink import MUTE_AUDIO, Projector
from pypjlink.projector import ProjectorError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    STATE_OFF,
    STATE_ON
)

from .const import DOMAIN
from .exceptions import CannotConnect, PoweredOff, PasswordInvaid, AuthenticationRequired

PLATFORMS = ["media_player", "sensor"]

_LOGGER = logging.getLogger(__name__)




async def validate_projector(
    hass: HomeAssistant, host, password, port=4352, encoding="utf-8", DEFAULT_TIMEOUT=10
):
    """Validate the given projector host allows us to connect."""

    epson_proj = Projector.from_address(
        host,port,encoding,DEFAULT_TIMEOUT
    )
    
    try:
        _LOGGER.debug(f"Projector.from_address -> {epson_proj}")
        authenticate = epson_proj.authenticate(password)
        _LOGGER.debug(f"Projector authenticate -> {authenticate}")
        _LOGGER.debug(authenticate)
        if authenticate == False:
            raise PasswordInvaid
        elif authenticate == None:
            raise AuthenticationRequired
        else:
            _LOGGER.debug(f"Projector -> {epson_proj.get_power()}")
            pwstate = epson_proj.get_power()
            if pwstate in ("off"):
                _LOGGER.debug("Projector is poweroff")
                #raise PoweredOff
    except ProjectorError as err:
        if str(err) == "unavailable time":
            _LOGGER.debug("Cannot connect to projector")
            raise CannotConnect
        else:
            raise

    return epson_proj


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up epson from a config entry."""
    projector = await validate_projector(
        hass=hass,
        host=entry.data[CONF_HOST],
        password=entry.data[CONF_PASSWORD]
    )
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = projector
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
