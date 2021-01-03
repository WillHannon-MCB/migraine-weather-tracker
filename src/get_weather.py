"""
This module uses the One Call API from OpenWeather (https://openweathermap.org/api/one-call-api) 
to get historic/current/forcast data for the barometric pressure and humidity.
"""

from pyowm.owm import OWM

def get_api_key(filepath):
    """Read a local file with your API key."""
    api = []
    with open(filepath) as f:
        for line in f:
            api.append(line.strip())
    assert len(api) == 1, "API key should be only one line long."
    return api[0]

# TEST: test the API works 
# Coordinates for Seattle (lat, lon)
coords = (47.6062,-122.3321)
key = get_api_key("API.txt")
owm = OWM(key)
mgr = owm.weather_manager()
test_dict = mgr.one_call(lat = coords[0], lon = coords[1])
for i in test_dict.forecast_hourly:
    print((i.reference_time('iso')))
