"""Platform for sensor integration."""
from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers import entity_platform
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Epson projector from a config entry."""

    entry_id = config_entry.entry_id
    _LOGGER.debug(f"ProjectorSensor_entry_id -> {entry_id}")
    projector = hass.data[DOMAIN][entry_id]

    Lamps_Sensor_Entity = Lamps_Sensor(
        projector=projector,
        name=config_entry.title,
        entry=config_entry,
    )
    OnOff_Sensor_Entity = OnOff_Sensor(
        projector=projector,
        name=config_entry.title,
        entry=config_entry,
    )
    Errors_Sensor_Entity = Errors_Sensor(
        projector=projector,
        name=config_entry.title,
        entry=config_entry,
    )
    Input_Source_Sensor_Entity = Input_Source_Sensor(
        projector=projector,
        name=config_entry.title,
        entry=config_entry,
    )
    
    async_add_entities([Lamps_Sensor_Entity, OnOff_Sensor_Entity,Errors_Sensor_Entity,Input_Source_Sensor_Entity], True)
    platform = entity_platform.async_get_current_platform()




class Lamps_Sensor(SensorEntity):
    """Representation of a PJLink device."""

    def __init__(self, projector, name, entry, unique_id=None):
        """Initialize entity to control Epson projector."""
        self._projector = projector
        self._entry = entry
        self._name = name
        self._lamps = None
        self._unique_id = unique_id

    async def set_unique_id(self):
        """Set unique id for projector config entry."""

        if self._unique_id:
            return False
        if uid := random.random():
            self.hass.config_entries.async_update_entry(self._entry, unique_id=uid)
            registry = async_get_entity_registry(self.hass)
            old_entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, self._entry.entry_id
            )
            if old_entity_id is not None:
                registry.async_update_entity(old_entity_id, new_unique_id=uid)
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._entry.entry_id)
            )
            return True

    async def async_update(self):
        """Get the latest state from the device."""
        
        lamps_state = self._projector.get_lamps()
        _LOGGER.debug("Projector lamps_state11111: %s", lamps_state)
        if lamps_state != None:
            self._lamps = ('灯泡已使用 '+str(lamps_state[0][0])+' 小时')
        else:
            self._lamps = "投影机异常"


    @property
    def name(self):
        """Return the name of the device."""
        rename = self._name+'灯泡'
        return rename 

    @property
    def state(self):
        """Return the state of the device."""
        return self._lamps


class OnOff_Sensor(SensorEntity):
    """Representation of a PJLink device."""
    
    def __init__(self, projector, name, entry, unique_id=None):
        """Initialize entity to control Epson projector."""
        self._projector = projector
        self._entry = entry
        self._name = name
        self._unique_id = unique_id
        self._pwstate = None

    async def set_unique_id(self):
        """Set unique id for projector config entry."""

        if self._unique_id:
            return False
        if uid := random.random():
            self.hass.config_entries.async_update_entry(self._entry, unique_id=uid)
            registry = async_get_entity_registry(self.hass)
            old_entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, self._entry.entry_id
            )
            if old_entity_id is not None:
                registry.async_update_entity(old_entity_id, new_unique_id=uid)
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._entry.entry_id)
            )
            return True

    async def async_update(self):
        """Get the latest state from the device."""

        pwstate = self._projector.get_power()
        _LOGGER.debug("Projector pwstate11111: %s", pwstate)
        if pwstate in ("warm-up"):
            self._pwstate = "预热"
        elif pwstate in ("on"):
            self._pwstate = "开"
        else:
            self._pwstate = "关"

    @property
    def name(self):
        """Return the name of the device."""
        rename = self._name+'开关'
        return rename 

    @property
    def state(self):
        """Return the state of the device."""
        return self._pwstate

class Errors_Sensor(SensorEntity):
    """Representation of a PJLink device."""

    def __init__(self, projector, name, entry, unique_id=None):
        """Initialize entity to control Epson projector."""
        self._projector = projector
        self._entry = entry
        self._name = name
        self._unique_id = unique_id
        self._errors = None

    async def set_unique_id(self):
        """Set unique id for projector config entry."""

        if self._unique_id:
            return False
        if uid := random.random():
            self.hass.config_entries.async_update_entry(self._entry, unique_id=uid)
            registry = async_get_entity_registry(self.hass)
            old_entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, self._entry.entry_id
            )
            if old_entity_id is not None:
                registry.async_update_entity(old_entity_id, new_unique_id=uid)
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._entry.entry_id)
            )
            return True

    async def async_update(self):
        """Get the latest state from the device."""

        errors = self._projector.get_errors()
        _LOGGER.debug("Projector errors11111: %s", errors)
        if errors['fan'] == "ok" and errors['lamp'] == "ok" and errors['temperature'] == "ok" and errors['cover'] == "ok" and errors['filter'] == "ok" and errors['other'] == "ok":
            self._errors = "风扇、灯泡、温度、过滤网等状态全部正常"
        elif errors['fan'] != "ok":
            self._errors = "风扇异常"
        elif errors['lamp'] != "ok":
            self._errors = "灯泡异常"
        elif errors['temperature'] == "ok":
            self._errors = "温度异常"
        elif errors['cover'] == "ok":
            self._errors = "cover异常"
        elif errors['filter'] == "ok":
            self._errors = "过滤网异常"
        elif errors['other'] == "ok":
            self._errors = "其他异常"
        else:
            self._errors = "出现监控条件外异常"

    @property
    def name(self):
        """Return the name of the device."""
        rename = self._name+'传感器'
        return rename 

    @property
    def state(self):
        """Return the state of the device."""
        return self._errors

def format_input_source(input_source_name, input_source_number):
    """Format input source for display in UI."""
    return f"{input_source_name} {input_source_number}"
    
class Input_Source_Sensor(SensorEntity):
    """Representation of a PJLink device."""

    def __init__(self, projector, name, entry, unique_id=None):
        """Initialize entity to control Epson projector."""
        self._projector = projector
        self._entry = entry
        self._name = name
        self._unique_id = unique_id
        self._inputs = None

    async def set_unique_id(self):
        """Set unique id for projector config entry."""

        if self._unique_id:
            return False
        if uid := random.random():
            self.hass.config_entries.async_update_entry(self._entry, unique_id=uid)
            registry = async_get_entity_registry(self.hass)
            old_entity_id = registry.async_get_entity_id(
                "sensor", DOMAIN, self._entry.entry_id
            )
            if old_entity_id is not None:
                registry.async_update_entity(old_entity_id, new_unique_id=uid)
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._entry.entry_id)
            )
            return True

    async def async_update(self):
        """Get the latest state from the device."""

        inputs = self._projector.get_inputs()
        _LOGGER.debug("Projector inputs11111: %s", inputs)
        self._source_name_mapping = {format_input_source(*x): x for x in inputs}
        self._source_list = sorted(self._source_name_mapping.keys())

        pwstate = self._projector.get_power()
        if pwstate in ("on", "warm-up"):
            if format_input_source(*self._projector.get_input()) == "DIGITAL 2":
                self._current_source = "当前输入源为HDMI 1"
            else:
                self._current_source = format_input_source(*self._projector.get_input())
        else:
            self._current_source = "无信号输入"

    @property
    def name(self):
        """Return the name of the device."""
        rename = self._name+'信号源'
        return rename 

    @property
    def state(self):
        """Return current input source."""
        return self._current_source

    @property
    def source_list(self):
        """Return all available input sources."""
        return self._source_list

    def select_source(self, source):
        """Set the input source."""
        source = self._source_name_mapping[source]
        self._projector.set_input(*source)