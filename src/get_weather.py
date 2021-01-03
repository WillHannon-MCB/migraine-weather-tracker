"""
This module uses the One Call API from OpenWeather (https://openweathermap.org/api/one-call-api) 
to get historic/current/forcast data for the barometric pressure and humidity.
"""

from pyowm.owm import OWM
from pyowm.utils import timestamps
from datetime import datetime, timedelta, timezone
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd

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

    def _get_forecast(self):
        """Get forecast weather as list of tuples."""
        # Access the One-Call API forecast
        one_call_forecast = self.mgr.one_call(self.lat, self.lon) 
        hourly_weather = {(weather.reference_time('iso'), weather.pressure['press']) for weather in one_call_forecast.forecast_hourly}
        daily_weather = {(weather.reference_time('iso'), weather.pressure['press']) for weather in one_call_forecast.forecast_daily}
        return hourly_weather.union(daily_weather)
    
    def _get_history(self):
        """Get the historic weather."""
        # Get the historic data is a 48hr interval starting 48hrs ago.
        two_day_epoch = int((datetime.now() - timedelta(hours=48)).replace(tzinfo=timezone.utc).timestamp())
        # Access the One-Call API history
        one_call_history = self.mgr.one_call_history(self.lat, self.lon, dt=two_day_epoch)
        hourly_weather = {(weather.reference_time('iso'), weather.pressure['press']) for weather in one_call_history.forecast_hourly}
        return hourly_weather

    def _combine_forecast_history(self):
        """Get and combine the forecast and history"""
        history = self._get_history()
        forecast = self._get_forecast()
        combined = list(history.union(forecast))
        return [(dateutil.parser.isoparse(time), press) for time, press in combined]
    
    def plot_pressure(self):
        """Plot the pressure over time."""
        combined_dataframe = pd.DataFrame(self._combine_forecast_history(), columns=['Time','Press'])
        combined_dataframe.set_index('Time').plot()
        plt.show()



# TEST: test the API works 
# Coordinates for Seattle (lat, lon)
coords = (47.6062,-122.3321)
key = get_api_key("API.txt")

LocalWeather(key,coords).plot_pressure()


