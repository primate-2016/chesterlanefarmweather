import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def format_current_weather(weather_dict: dict) -> str:
    '''
    return a properly formatted string for Alexa to say
    '''

    try:
        temp = weather_dict['observations'][0]['uk_hybrid']['temp']
        day_rain = weather_dict['observations'][0]['uk_hybrid']['precipTotal']
        wind_speed = weather_dict['observations'][0]['uk_hybrid']['windSpeed']
        wind_chill = weather_dict['observations'][0]['uk_hybrid']['windChill']
        uv_index = int(weather_dict['observations'][0]['uk_hybrid']['uv'])

    except KeyError:
        logger.error('Did not get properly formatted weather data from API')
        return 'Something went wrong getting weather data, please try again'

    temp_comment = f'the temperature is {temp} degrees but it feels like {int(temp) - int(wind_chill)} degress' if int(wind_chill) >= 4 else f'the temperature is {temp} degrees'

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

    return temp_comment + uv_index_comment + misc_comment
