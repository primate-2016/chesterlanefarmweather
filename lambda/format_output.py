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
        wind_chill = weather_dict['observations'][0]['uk_hybrid']['windChill']
        uv_index = int(weather_dict['observations'][0]['uv'])

    except KeyError as e:
        logger.error(f'Did not get properly formatted weather data from API: {e}')
        return 'Something went wrong getting weather data, please try again'

    temp_comment = f'the temperature now is {temp} degrees but it feels like {int(temp) - int(wind_chill)} degrees' if int(wind_chill) >= 3 else f'the temperature now is {temp} degrees'

    # UV index https://www.epa.gov/sites/default/files/documents/uviguide.pdf
    uv_index_comment = ', the U V index is '
    if uv_index in range(0, 3):
        uv_index_comment += 'low'
    elif uv_index in range(3, 6):
        uv_index_comment += 'moderate'
    elif uv_index in range(6, 8):
        uv_index_comment += 'high, get the sunscreen out!'
    elif uv_index in range(8, 11):
        uv_index_comment += 'very high, factor 50 today!'
    elif uv_index >= '11':
        uv_index_comment += 'extreme, stay in the shade!'
    else:
        uv_index_comment += 'out of range'

    misc_comment = f', the total rainfall today is {day_rain} millimeters, the windspeed is {wind_speed} kilometers per hour'

    output = temp_comment + uv_index_comment + misc_comment
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
