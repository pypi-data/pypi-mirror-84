"""A Python Wrapper to communicate with a Meteobridge Data Logger."""
from pymeteobridgeio.client import Meteobridge
from pymeteobridgeio.errors import (
    InvalidCredentials,
    RequestError,
    ResultError,
)
from pymeteobridgeio.const import (
    DEVICE_CLASS_NONE,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_RAIN,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_WIND,
    DEVICE_TYPE_BINARY_SENSOR,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_NONE,
    SUPPORTED_LANGUAGES,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_TYPE_DIST_KM,
    UNIT_TYPE_DIST_MI,
    UNIT_TYPE_PRESSURE_HPA,
    UNIT_TYPE_PRESSURE_INHG,
    UNIT_TYPE_PRESSURE_MB,
    UNIT_TYPE_RAIN_MM,
    UNIT_TYPE_RAIN_IN,
    UNIT_TYPE_TEMP_CELCIUS,
    UNIT_TYPE_TEMP_FAHRENHEIT,
    UNIT_TYPE_WIND_KMH,
    UNIT_TYPE_WIND_MS,
    UNIT_TYPE_WIND_MPH,
)