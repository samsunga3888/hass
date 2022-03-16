"""The errors of Epson integration."""
from homeassistant import exceptions


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class PoweredOff(exceptions.HomeAssistantError):
    """Error to indicate projector is off."""


class PasswordInvaid(exceptions.HomeAssistantError):
    """Error to indicate projector authenticate is fail."""

class AuthenticationRequired(exceptions.HomeAssistantError):
    """Error to indicate projector authenticate is unable."""