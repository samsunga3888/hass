"""Config flow for epson integration."""
import logging
import random
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT,CONF_PASSWORD

from . import validate_projector
from .const import DOMAIN
from .exceptions import CannotConnect, PoweredOff, PasswordInvaid, AuthenticationRequired

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_NAME, default=DOMAIN): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for epson."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        _LOGGER.debug(f"validate_projector -> {user_input}")
        if user_input is not None:
            _LOGGER.debug(f"validate_projector1 -> {user_input}")
            try:
                projector = await validate_projector(
                    hass=self.hass,
                    host=user_input[CONF_HOST],
                    password=user_input[CONF_PASSWORD]
                )
                _LOGGER.debug(f"validate_projector2 -> {projector}")
            except PasswordInvaid:
                _LOGGER.debug(f"validate_projectorPasswordInvaid -> {PasswordInvaid}")
                _LOGGER.warning(
                    "You need to check projector password for initial configuration"
                )
                errors["base"] = "password_invaid"
            except AuthenticationRequired:
                _LOGGER.debug(f"validate_projectorAuthenticateInvaid -> {AuthenticationRequired}")
                _LOGGER.warning(
                    "You need to enable projector Authenticate for initial configuration"
                )
                errors["base"] = "authenticate_invaid"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except PoweredOff:
                _LOGGER.debug(f"validate_projectorPoweredOff -> {PoweredOff}")
                _LOGGER.warning(
                    "You need to turn ON projector power for initial configuration"
                )
                errors["base"] = "powered_off"
            else:
                serial_no = random.random()
                await self.async_set_unique_id(serial_no)
                self._abort_if_unique_id_configured()
                user_input.pop(CONF_PORT, None)
                return self.async_create_entry(
                    title=user_input.pop(CONF_NAME), data=user_input
                )
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
