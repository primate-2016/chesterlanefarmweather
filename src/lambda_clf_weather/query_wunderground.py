import requests
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api_key = os.getenv('API_KEY')
station_id = os.getenv('STATION_ID')
lat = os.getenv('LAT')
lon = os.getenv('LON')

def get_current_weather() -> dict:
    '''
    Return a dict of the current weather conditions
    https://docs.google.com/document/d/1KGb8bTVYRsNgljnNH67AMhckY8AQT2FVwZ9urj8SWBs/edit
    '''

    url = 'https://api.weather.com/v2/pws/observations/current'
    current_weather_params = {
        'stationId': station_id,
        'format': 'json',
        'units': 'h',
        'apiKey': api_key
    }
    response = requests.request('GET', url, params=current_weather_params)

    try:
        return(json.loads(response.text))
    except json.decoder.JSONDecodeError as e:
        logger.error(f'Couldn\'t decode JSON, got this instead: {response.text}')
        raise e


def get_five_day_forecast() -> dict:
    '''
    Return a dict with a 5 day forecast for the PWS
    https://docs.google.com/document/d/1_Zte7-SdOjnzBttb1-Y9e0Wgl0_3tah9dSwXUyEA3-c/edit
    '''

    url = 'https://api.weather.com/v3/wx/forecast/daily/5day'
    forecast_params = {
        'geocode': f'{lat},{lon}',
        'format': 'json',
        'units': 'h',
        'language': 'en-GB',
        'apiKey': api_key
    }
    response = requests.request('GET', url, params=forecast_params)

    try:
        return(json.loads(response.text))
    except json.decoder.JSONDecodeError as e:
        logger.error(f'Couldn\'t decode JSON, got this instead: {response.text}')
        raise e


if __name__ == '__main__':
    print(get_current_weather())



# data = get_current_weather(pws_api_base_url, current_weather_params)
# print(data)

# data = get_five_day_forecast(forecast_api_base_url, forecast_params)
# print(data)
