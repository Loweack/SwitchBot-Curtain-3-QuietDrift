from homeassistant.const import CONF_ENTITY_ID
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

DOMAIN = "switchbot_curtain_3_quietdrift"

CONF_SPEED = 'speed'
CONF_POSITION = 'position'

# Speed Options
SPEED_QUIETDRIFT = "QuietDrift"
SPEED_SILENT = "Silent"
SPEED_NORMAL = "Normal"

SPEED_OPTIONS = [SPEED_QUIETDRIFT, SPEED_SILENT, SPEED_NORMAL]

SET_COVER_POSITION_SCHEMA = vol.Schema({
    vol.Required(CONF_ENTITY_ID): cv.entity_ids,
    vol.Required(CONF_POSITION): vol.Range(min=0, max=100),
    vol.Optional(CONF_SPEED, default=SPEED_NORMAL): vol.In(SPEED_OPTIONS),
})
