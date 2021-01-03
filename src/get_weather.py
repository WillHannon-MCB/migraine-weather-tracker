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


class LocalWeather:
    """Class to hold the weather in user location.
    
    Arguments:
    ----------
    key: Your API key for OpeWeather
    coords: A tuple for the lat. & lon. of your location
    """
    def __init__(self, key, coords):
        self.key = key
        self.lat, self.lon = coords
        self.owm = OWM(self.key)
        self.mgr = self.owm.weather_manager()

# TEST: test the API works 
# Coordinates for Seattle (lat, lon)
coords = (47.6062,-122.3321)
key = get_api_key("API.txt")

#test_dict = mgr.one_call(lat = coords[0], lon = coords[1])

print(LocalWeather(key, coords).lat)
