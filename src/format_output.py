import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def format_current_weather(weather_dict: dict) -> str:
    '''
    return a properly formatted string for Alexa to say 
    '''

    logger.info(f'The weather data dict is:{weather_dict}')

    try:
        temp = weather_dict['observations'][0]['uk_hybrid']['temp']
        day_rain = weather_dict['observations'][0]['uk_hybrid']['precipTotal']
        wind_speed = weather_dict['observations'][0]['uk_hybrid']['windSpeed']
        wind_gust = weather_dict['observations'][0]['uk_hybrid']['windGust']
        temp_with_wind_chill = weather_dict['observations'][0]['uk_hybrid']['windChill']
        uv_index = int(weather_dict['observations'][0]['uv'])
        humidity = weather_dict['observations'][0]['humidity']

    except KeyError as e:
        logger.error(f'Did not get properly formatted weather data from API: {e}')
        return 'Something went wrong getting weather data, please try again'

    temp_comment = f'The temperature now is {temp} degrees but it feels like {temp_with_wind_chill} degrees due to wind chill. ' if int(temp) - int(temp_with_wind_chill) > 1 else f'the temperature now is {temp} degrees. '

    # UV index https://www.epa.gov/sites/default/files/documents/uviguide.pdf
    uv_index_comment = 'The U V index is '
    if uv_index in range(0, 3):
        uv_index_comment += 'low. '
    elif uv_index in range(3, 6):
        uv_index_comment += 'moderate. '
    elif uv_index in range(6, 8):
        uv_index_comment += 'high, get the sunscreen out! '
    elif uv_index in range(8, 11):
        uv_index_comment += 'very high, factor 50 today! '
    elif uv_index >= '11':
        uv_index_comment += 'extreme, stay in the shade! '
    else:
        uv_index_comment += 'out of range. '

    rain_comment = f'There has been no rainfall recorded today and the humidity is {humidity} percent. ' if int(day_rain) == 0.0 else f'The total rainfall today is {day_rain} millimeters and the humidity is {humidity} percent. '
    wind_comment = f'The windspeed is {wind_speed} miles per hour. ' if int(wind_speed) == int(wind_gust) else f'The windspeed is {wind_speed} miles per hour with gusts at {wind_gust} miles per hour. '

    output = temp_comment + uv_index_comment + rain_comment + wind_comment
    logger.info(f'speech output being returned is: {output}')
    return output


def format_forecast(forecast_dict: dict) -> str:
    '''
    return a properly formatted string for Alexa to say
    '''

    logging.info(f'The forecast dict is: {forecast_dict}')

    try:
        forecast_data = forecast_dict['daypart'][0]
    except KeyError as e:
        logger.error(f'Did not get properly formatted forecast data from API: {e}')
        raise e

    # create a dict of day to forecast
    day_to_forecast_dict = {}
    for day_name in forecast_data['daypartName']:
        index = forecast_data['daypartName'].index(day_name)
        day_to_forecast_dict[day_name] = forecast_data['narrative'][index]

    # clear any 'None' values - API returns 'null' if you are part way through current time period
    for k in dict(day_to_forecast_dict).keys():
        if k is None:
            del day_to_forecast_dict[k]

    logger.info(f'Day to forecast dict is: {day_to_forecast_dict}')

    output = ''
    for k, v in day_to_forecast_dict.items():
        output += f'{k}, {v} '

    logger.info(f'speech output being returned is: {output}')
    return output
