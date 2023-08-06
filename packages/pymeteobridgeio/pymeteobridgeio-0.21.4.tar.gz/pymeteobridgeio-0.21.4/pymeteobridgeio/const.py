"""Constant Definitions for MeteoBridge."""

BASE_URL = "https://swd.weatherflow.com/swd/rest/observations"

DEFAULT_TIMEOUT = 10

DEVICE_CLASS_NONE = "none"
DEVICE_CLASS_DISTANCE = "distance"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_RAIN = "rain"
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_WIND = "wind"
DEVICE_CLASS_COLD = "cold"

DEVICE_TYPE_SENSOR = "sensor"
DEVICE_TYPE_BINARY_SENSOR = "binary_sensor"
DEVICE_TYPE_NONE = "none"

UNIT_SYSTEM_METRIC = "metric"
UNIT_SYSTEM_IMPERIAL = "imperial"

UNIT_TYPE_DIST_KM = "km"
UNIT_TYPE_DIST_MI = "mi"
UNIT_TYPE_PRESSURE_HPA = "hPa"
UNIT_TYPE_PRESSURE_INHG = "inHg"
UNIT_TYPE_PRESSURE_MB = "mb"
UNIT_TYPE_RAIN_MM = "mm"
UNIT_TYPE_RAIN_IN = "in"
UNIT_TYPE_TEMP_CELCIUS = "°C"
UNIT_TYPE_TEMP_FAHRENHEIT = "°F"
UNIT_TYPE_WIND_KMH = "km/h"
UNIT_TYPE_WIND_MS = "m/s"
UNIT_TYPE_WIND_MPH = "mph"


SUPPORTED_LANGUAGES = [
    "en",
    "da",
    "nl",
    "es",
    "de",
    "fr",
    "it",
    "nb",
    "sv",
    "pt",
    "pl",
]
